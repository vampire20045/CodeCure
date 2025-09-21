// Example JavaScript file with issues for CodeCure testing

function problemFunction() {
    console.log("Debug message");  // Should suggest proper logging
    
    let value = "5";
    if (value == 5) {  // Should suggest using === instead
        console.log("Values match");
    }
    
    // TODO: Add input validation
    
    return value;
}

function anotherFunction() {
    console.log("Another debug statement");
    
    let result = problemFunction();
    
    // This line has trailing spaces    
    
    if (result != undefined) {  // Should suggest using !== instead
        return result;
    }
}

// Very long line that exceeds reasonable length and should trigger a warning about line length in the code
let veryLongVariableName = "This is a very long line that should trigger a line length warning from CodeCure";

anotherFunction();