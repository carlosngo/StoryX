$(document).ready(() => {
    var elements = [
        [],
        [],
        [],
        [],
        []
    ]
    var history = []

    var currentObject = {}

    const DIALOGUE = 0
    const CHARACTER = 1
    const PROP = 2
    const ACTION = 3
    const TRANSITION = 4
    const CONTENT_START = 0
    const CONTENT_END = 1
    const SPEAKER_START = 2
    const SPEAKER_END = 3
    const CHAR_START = 0
    const CHAR_END = 1
    const PROP_START = 0
    const PROP_END = 1

    var element_idx = -1
    var element_labels = ["dialogues", "characters", "props", "action lines", "scene transitions"]
    var instruction_idx = 0
    var instruction_labels = [
        ["content_start", "content_end", "speaker_start", "speaker_end"], 
        ["char_start", "char_end"],
        ["prop_start", "prop_end"],
        ["action_sent"],
        ["transition_sent"],
    ]

    var instructions = [
        // Dialogue instructions
        [
            'Click on the double quotes (") that marks the start of a dialogue.',
            'Click on the double quotes (") that marks the end of the dialogue.',
            'Click on the word that marks the start of the dialogue speaker.',
            'Click on the word that marks the end of the dialogue speaker.',
        ],
        // Character instructions
        [
            'Click on the word that marks the start of a character mention.',
            'Click on the word that marks the end of a character mention.',
        ],
        // Prop instructions
        [
            'Click on the word that marks the start of a prop mention.',
            'Click on the word that marks the end of a prop mention.',
        ],
        // Action instructions
        [
            'Click on a sentence that is an action line.',
        ],
        // Scene Transition instructions
        [
            'Click on a sentence that marks the start of a new scene.',
        ],
    ]

    // order of notes does not matter
    var notes = [
        // Dialogue notes
        [   
            // First dialogue instruction (see above) notes
            [
                'Treat multi-paragraph dialogue as one big chunk of dialogue. The opening quotes will be the first double quotes, and the ending quotes will be the last double quotes. Ignore the opening quotes in-between.'
            ],
            // Second dialogue instruction notes
            [
                'Treat multi-paragraph dialogue as one big chunk of dialogue. The opening quotes will be the first double quotes, and the ending quotes will be the last double quotes. Ignore the opening quotes in-between.'
            ],
            [
                'For example, if Big Bad Wolf is the speaker, Big will be the start of a character mention.',
                'The start and end of the speaker can be the same word.',
                'A speaker is not limited to proper nouns.',
                'If the speaker is not explicitly stated, please choose the nearest speaker before the dialogue content.',
            ],
            [
                'For example, if Big Bad Wolf is the speaker, Wolf will be the end of a character mention.',
                'The start and end of the speaker can be the same word.',
                'A speaker is not limited to proper nouns. Pronouns and common nouns can be the speaker.',
                'If the speaker is not explicitly stated, please select the nearest speaker before the dialogue content.',
            ],
        ],
        // Character notes
        [
            [
                "Characters are not limited to proper nouns. Characters can also be common nouns but not pronouns."
            ],
            [

            ],
        ],
        // Prop notes
        [
            [

            ],
            [

            ],
        ],
        // Action notes
        [
            [

            ],
        ],
        // Scene Transition notes
        [
            [

            ],
        ],
    ]

    nextElement()

    $("#btn-copy").on('click', () => copy())
    $("#btn-proceed").on('click', () => nextElement())
    $("#btn-annotate").on('click', () => annotate())
    $("#btn-undo").on('click', () => undo())

    $(".token").on('click', function() {
        var idx = $(this).attr('data-idx')
        let key = instruction_labels[element_idx][instruction_idx]
        if (key[key.length - 1] == 'd') {
            let startKey = key.substr(0, key.length - 4)
            let startIdx = parseInt(currentObject[startKey + "_start"])
            let curIdx = parseInt(idx)
            let curElement = $(this)
            while (curIdx != startIdx) {
                $(curElement).css('background-color', '#add8e6')
                curElement = $(curElement).prev()
                curIdx--
            }
        } else {
            $(this).css('background-color', '#add8e6')
        }
        selectElement(idx)
        nextInstruction()
    })

    $(".sentence").on('click', function() {
        var idx = $(this).attr('data-idx')
        $(this).css('background-color', '#add8e6')
        selectElement(idx);
        nextInstruction()
    })


    function annotate() {
        var output = ""
        for(let i = 0; i < elements[element_idx].length; i++) {
            element = elements[element_idx][i];
            let j = 0;
            for (let key in element) {
                if (j > 0) {
                    output += " "
                }
                if (element.hasOwnProperty(key)) {
                    output += element[key]
                }
                j++;
            }
            output += "\n"
        }
        $("#output").text(output)
        // if (element_idx == DIALOGUE) {
        // } else if (element_idx == CHARACTER) {  
        // } else if (element_idx == PROP) {
        // } else if (element_idx == ACTION) {
        // } else if (element_idx == TRANSITION) {
        // }
    }

    function undo() {
        if (instruction_idx == 0) {
            currentObject = elements[element_idx].pop()
            instruction_idx = instruction_labels[element_idx].length
        } 
        // console.log('token')
        var key = instruction_labels[element_idx][instruction_idx - 1]
        // console.log(key)
        var idx = currentObject[key]
        if (element_idx < ACTION) {
            
            var query = ".token[data-idx='" + idx + "']";
            // console.log(query)
            var curElement = $(query)
            // console.log(curElement)
            if (key[key.length - 1] == 'd') {
                console.log('end')
                var startKey = key.substr(0, key.length - 4)
                var startIdx = parseInt(currentObject[startKey + "_start"])
                var curIdx = parseInt(idx)
                while (curIdx != startIdx) {
                    $(curElement).css('background-color', 'transparent')
                    curElement = $(curElement).prev()
                    curIdx--
                }
            } else {
                // console.log('start')
                $(curElement).css('background-color', 'transparent')
            }
        } else {
            // console.log('sent')
            var query = ".sentence[data-idx='" + idx + "']";
            var curElement = $(query)
            $(curElement).css('background-color', 'transparent')
        }

        delete currentObject[key]

        previousInstruction()
        if (history.length == 0 && Object.keys(currentObject).length == 0) {
            $("#btn-undo").prop('disabled', true)
        } 
    }
    
    function copy() {
        textarea = document.getElementById("output")
        textarea.focus()
        textarea.select()
        var success = document.execCommand('copy')
        if (success == true) {
            $("#btn-copy").removeClass("btn-light")
            $("#btn-copy").addClass("btn-success")
            $("#btn-copy").html('<i class="fa fa-clipboard mr-2"></i>Copied to Clipboard!')
            setTimeout(function(){
                $("#btn-copy").addClass("btn-light")
                $("#btn-copy").removeClass("btn-success")
                $("#btn-copy").html('<i class="fa fa-clipboard mr-2"></i>Copy to Clipboard')
            }, 1000)
        }
    }

    function selectElement(idx) {
        currentObject[instruction_labels[element_idx][instruction_idx]] = idx
        if (instruction_idx == instruction_labels[element_idx].length - 1) {
            console.log(currentObject);
            history.push(currentObject)
            elements[element_idx].push(currentObject)
            currentObject = {}
        }
        $("#btn-undo").prop('disabled', false)
    }

    function nextElement() {
        if (element_idx == TRANSITION) {
            $("#form-finish").submit()
        }
        element_idx++
        instruction_idx = -1
        currentObject = {}
        history = []
        nextInstruction()
        $("#output").text('')
        $("#btn-undo").prop('disabled', true)
        $(".sentence").css('background-color', 'transparent')
        $(".token").css('background-color', 'transparent')
        $(".story-element").text(element_labels[element_idx])
        if (element_idx == TRANSITION) {
            $("#btn-proceed").html('<i class="fa fa-share mr-2"></i>Finish')
        } 
        if (element_idx == TRANSITION || element_idx == ACTION) {
            $("#sentence-view").show()
            $("#token-view").hide()
        } else {
            $("#sentence-view").hide()
            $("#token-view").show()
        }

    }

    function loadInstruction() {
        $("#instruction").text(instructions[element_idx][instruction_idx])    
    }

    function loadNotes() {
        var lastNote = $("#notes").children().last()
        $("#notes").empty()
        // console.log(lastNote)
        for (let i = 0; i < notes[element_idx][instruction_idx].length; i++) {
            var note = $('<li></li>')
            note.text(notes[element_idx][instruction_idx][i])
            // console.log(note)
            $("#notes").append(note)
        }
        $("#notes").append(lastNote)
    }

    function nextInstruction() {
        if (instruction_idx == instructions[element_idx].length - 1) {
            instruction_idx = -1
        }
        instruction_idx++
        loadInstruction()
        loadNotes()
    }

    function previousInstruction() {
        if (instruction_idx == 0) {
            instruction_idx = instructions[element_idx].length
        }
        instruction_idx--
        loadInstruction()
        loadNotes()
    }
})