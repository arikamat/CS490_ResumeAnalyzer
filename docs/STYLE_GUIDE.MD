# Style Guide

*All implemented tasks must have comments on top of file/group of code describing what has been implemented, input, and output (including types if applicable)*

## Front End
  
Basic Rules
- Only one component per file 
- JSX syntax  

React Components should follow 
- File names should be Pascal Case **`RegistrationForm.jsx`**
- Use .jsx for file extensions
- Use Pascal Case for component naming **`RegistrationForm`**
- Use Functional Componenets 
- Camel case for variables/consts **`loginVar`**
- Camel case for prop names **`propOne`**
- Have alt for all img tags **`<img src="thing.jpg" alt="This is a thing"/>`**
- Use arrow functions to go over variables in loops or with mapping

Testing Naming Convention
- Use the same name as the component or module being tested, with a `.test.jsx` suffix.
  - Example: For `Button.jsx`, name the test file `Button.test.jsx`.

Test Description
- Use clear and descriptive `it` or `test` statements to describe what the test does.
  - Example:
    ```javascript
    it('renders the Button component', () => {
      // testimplemted 
    });
    ```

Test Grouping
- Group related tests using `describe` blocks.
  - Example when testing a **`Button Component`**:
    ```javascript
    describe('Button component', () => {
      it('renders correctly', () => {
        // render events 
      });

      it('handles click events', () => {
        // click events
      });
    });
    ```

## Back End
