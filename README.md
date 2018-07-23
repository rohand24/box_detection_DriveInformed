Box Detection
=============

Guidelines
----------
* Organize, test, and document like you would on Production
* Send us a link to the hosted repository (Github, Bitbucket, ...)

Task
----
Create a service that will detect all the boxes in a given document.

It should take the following paramters:
* `input_file`: URL or a Local file path of the input document in which to detect the boxes
* `output_file`: Local file path of the output document in which to draw the detected boxes

Apart from drawing the boxes in the `output_file`, the service should also return the co-ordinates of the detected boxes in JSON format.

Example Response:
```
{
    "boxes": [
        {
            "points": [
                [
                    90,
                    838
                ],
                [
                    75,
                    838
                ],
                [
                    75,
                    851
                ],
                [
                    90,
                    851
                ],
                [
                    90,
                    838
                ]
            ]
        },
        {
            "points": [
                [
                    327,
                    840
                ],
                [
                    313,
                    840
                ],
                [
                    313,
                    853
                ],
                [
                    327,
                    853
                ],
                [
                    327,
                    840
                ]
            ]
        },
        .
        .
    ]
}
```


Examples
--------
For your convinenince, we have uploaded a few test documents in the `examples/inputs` directory. You can choose to test on those documents or any documents of your choosing.
We have also uploaded a few examples of what we expect the output files to look like in the `examples/outputs` directory. (The ID values inside each box is not required)

Running
-------
Obviously, we should be able to test your code. You have 2 options here:
* Create a `run_service.sh` script that will run a server locally on port `5000`
* Create a `README.md` in your repo with an example on how to run your service via the command line
