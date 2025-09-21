# Example Python file with various issues for testing CodeCure

import os

def problematic_function():
    # This function has several issues that CodeCure should detect
    
    print("Debug message")  # Should suggest using logging
    
    try:
        result = 10 / 0
    except:  # Bare except clause
        print("An error occurred")
    
    # TODO: Implement proper error handling
    
    unused_variable = "this is not used"
    
    very_long_line_that_exceeds_reasonable_length_and_should_trigger_a_warning_about_line_length_issues = "too long"
    
    return result  # This will cause an error since result might not be defined


def another_function():
    print("Another debug statement")
    
    # Some trailing whitespace here:   
    
    if True == False:  # Could suggest using 'is' for boolean comparison
        pass


if __name__ == "__main__":
    problematic_function()
    another_function()