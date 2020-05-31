# reviewTracker codeChallenge

This is a project made to answer gist.github.com/nvreynolds/c43c9c28c27f76488de2a85da33683ff

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the challengeProject. Should be using python3

```bash
pip3 install -r requirements.txt --user
```

## Summary

challengeProject app has 2 endpoint /reviews and /lenders
both of which are used to pull review data from lendingtree.com

/lenders/{id} takes in an id as part of the  request and has 2 required path params Name and VendorType

/reviews takes in a required param Link which should be a uri for the full request to the lendingtree website

## Usage
```bash
FLASK_APP=challengeProject/main.py flask run
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)