Script

`
{
  "script": "blabla"
}
`

Element Action Click

`
{
  "element": "send_button",
  "action": "click"
}
`

Element Action Read

`
{
  "element": "q1",
  "action": "read",
  "variable": "question_1"
}
`

Multi Element Action with random selection

`
{
  "elements": "q1_answers",
  "selector": "random",
  "action": "click"
}
`

Multi Element Action with foreach

`
{
  "elements": ["q1_a0", "q1_a1", "q1_a2", "q1_a3", "q1_a4", "q1_a5", "q1_a6"],
  "selector": "foreach",
  "action": "click"
}
`

Multi Element Action with reverse-foreach

`
{
  "elements": ["q1_a0", "q1_a1", "q1_a2", "q1_a3", "q1_a4", "q1_a5", "q1_a6"],
  "selector": "reverse-foreach",
  "action": "click"
}
`

Multi Element Action With Merge of control_collection and control

`
{
  "elements": ["all_radios", "q1"],
  "selector": "foreach",
  "action": "click"
},
`

Change Configuration

`
{
  "change_configuration": "config.json"
}
`