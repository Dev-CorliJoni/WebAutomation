# WebAutomation

## How to start
To start an automation, a configuration file must exist in the WebAutomation folder. An automation is started for each configuration file.

## Configuration

```json
{
  //'use_config' is an attribute that specifies whether the program should start this configuration or not.
  "use_config": true,
	
  //'hyperlink' is passed if a website is to be opened by the configuration
  //[optional] If available, a new website is opened. If not, the current website is used. 
  //If there is no current website, no "controls" or "control_collections" can be queried.
  "hyperlink": "https://www.google.com/",

  //'controls' In this section a key can be mapped to an x-path. When the configuration is started, the x-path element is queried. 
  "controls": {
    "cookies_deny_button": "//button/div[text()='Deny all']", 
    "cookies_accept_button": "//button/div[text()='Accept all']",
    "search_box": "//textarea[@type='search']"
  },

  //'control_collections' In this section a key can be mapped in two ways:
  //1. It is mapped to an x-path. When the application is started, the x-path element(s) is/are queried. 
  //2. It is mapped to an array of keys from the 'controls' section.
  "control_collections": {
    "cookie_buttons": ["cookies_deny_button", "cookies_accept_button"], 
    "all_text_areas": "//textarea"
  },
  
  //'automation' In this section the automation steps are defined. The steps in this array determine the sequence of automation.
  "automation": [				    
    
    // Step Name: element collection automation step
    // This step can be used to perform actions on multiple elements
    {
      //'elements' This attribute can be defined in two ways:
      //1. As an array of keys from the 'controls' or 'control_collections' section.
      "elements": ["cookies_deny_button", "cookies_accept_button"], 
      //2. As a key from the 'control_collections' section.
      "elements": "cookie_buttons",
      
      //'selector' This attribute determines which element of the specified 'elements' is affected by the 'action'.
      //Allowed values: [
      //                 "foreach",          // Each element is affected by the 'action'.
      //                 "reverse-foreach",  // Each element is affected by the 'action', but in reverse order.
      //                 "random"            // A randomly picked control is affected
      //                 ]
      "selector": "random",
      
      //'action' This attribute defines the action that this step should perform.
      //Allowed values: [
      //                 "click",          // Each element that is affected gets clicked.
      //                 "read",           // The text of each element that is affected is read and the contents are stored as an array.
      //                                   // Important: If 'read' is used, the 'variable' attribute must be specified.
      //                 "write"           // A text (the content of the 'value' attribute) is sent to each element, that is affected
      //                 ]
      "action": "click",
      
      //In this step, either none or one of the following two attributes can be specified
      
      //1. The 'value' attribute
      //[optional] Can only be used if the 'action' is "write"
      //If a previous step used the "read" 'action' and stored what was read in a 'variable', this variable can be inserted.
      //The insertion of a varaible starts with the $ sign. ($variable_name)
      //If special keys, like the ENTER key, are required they can be inserted. The keywords are coated by square Brackets [ENTER].
      //The allowed special keys are specified below.
      "value" : "Hello $my_var[ENTER]",
      
      //1. The 'variable' attribute
      //[optional] Can only be used if the 'action' is "read"
      //The content that is read is stored in this variable
      //No spaces or special characters are allowed inside of a name
      "variable" : "a"
    },

    // Step Name: element automation step
    // This step can be used to perform an action on a single element
    {
      //'element' This attribute is definded as a key from the 'controls' section.
      "element": "search_box",
      
      //'action' This attribute defines the action that this step should perform.
      //Allowed values: [
      //                 "click",          // The element gets clicked.
      //                 "read",           // The text of the element is read and the content is stored in a variable.
      //                                   // Important: If 'read' is used, the 'variable' attribute must be specified.
      //                 "write"           // A text (the content of the 'value' attribute) is sent to the element.
      //                 ]
      "action": "click",
      
      //In this step, either none or one of the following two attributes can be specified
      
      //1. The 'value' attribute
      //[optional] Can only be used if the 'action' is "write"
      //If a previous step used the "read" 'action' and stored what was read in a 'variable', this variable can be inserted.
      //The insertion of a varaible starts with the $ sign. ($variable_name)
      //If special keys, like the ENTER key, are required they can be inserted. The keywords are coated by square Brackets [ENTER].
      //The allowed keywords are specified below.
      "value" : "Hello $my_var[ENTER]",
      
      //1. The 'variable' attribute
      //[optional] Can only be used if the 'action' is "read"
      //The content that is read is stored in this variable
      //No spaces or special characters are allowed inside of a name
      "variable" : "a",
    },
    
    // Step Name: script automation step
    // This step can be used to call a python script
    {
      //'script' Path to the python script file
      "script": "C:\\scripts\\my_script.py"
    },

    // Step Name: change configuration automation step
    // The configuration gets switched to the specified configuration
    // This step is necessary if the page was previously redirected. The automation opens the new browser window after this call.
    {
      //'change_configuration' Path to the configuration file
      "change_configuration": "C:\\configurations\\configuration2.json"
    }
  ]
}
```