# viva-parse
Parse and dump VIVA conversations from json format to raw text and vice versa.

## Install:
```bash
pip install viva-parse
```

or from source:
```bash
pip install git+https://github.com/svenschultze/viva-parse
```

## Parse:
```python
import viva_parse

conversation = "<|prompter|> I want to book a room for monday at 3am<|endoftext|><|assistant|><|book_room|><[date]> monday<[time]> 3am<!return!> success!<|endofaction|> Success! I have booked a room for you.<|endoftext|>"
parsed = viva_parse.parse(conversation)
```

## Dump
```python
import viva_parse

conversation_json = [
    {
        'role': 'prompter', 
        'message': 'I want to book a room for monday at 3am'
    }, {
        'role': 'assistant', 
        'message': 'Success! I have booked a room for you.', 
        'actions': [
            {
                'name': 'book_room', 
                'params': {
                    'date': 'monday', 
                    'time': '3am'
                }, 
                'return': 'success!'
            }
        ]
    }
]

dumped = viva_parse.dump(conversation_json)
```