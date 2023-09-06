import json
import quart
import quart_cors
from quart import Quart, request, Response, send_file
import requests

import urllib.parse
import xml.etree.ElementTree as ET
from quickchart import QuickChart

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

@app.route("/chart/bar/<string:query>", methods=['GET'])
def get_bar_chart(query):
    try:
        # Get labels, colors, and title from query parameters
        xAxisLabel = request.args.get('xAxisLabel', 'X-Axis Label')
        yAxisLabel = request.args.get('yAxisLabel', 'Y-Axis Label')
        chartTitle = request.args.get("Title", "Sample Bar Chart")
        customLabels = request.args.get('customLabels', None)
        FontColor = request.args.get('Font Color','#00000')

        # Debugging print statements
        print(f"Received xAxisLabel: {xAxisLabel}")
        print(f"Received yAxisLabel: {yAxisLabel}")
        print(f"Received title: {chartTitle}")

        categoryLabel1 = request.args.get('categoryLabel1', 'Data Set 1')
        categoryLabel2 = request.args.get('categoryLabel2', 'Data Set 2')
        categoryLabel3 = request.args.get('categoryLabel3', 'Data Set 3')
        categoryLabel4 = request.args.get('categoryLabel4', 'Data Set 4')

        color1 = request.args.get('color1', '#3498db')  # Default to a shade of blue
        color2 = request.args.get('color2', '#2ecc71')  # Default to a shade of green
        color3 = request.args.get('color3', '#e74c3c')  # Default to a shade of red
        color4 = request.args.get('color4', '#e74c3c')  # Default to a shade of red
        
        # Parse the query to get chart parameters
        datasets = query.split('|')
        data_points1 = list(map(int, datasets[0].split(',')))
        if customLabels:
            labels = customLabels.split(',')
        else:
            labels = [f"Point {i}" for i in range(1, len(data_points1) + 1)]

        # Prepare chart configuration
        config = {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": categoryLabel1,
                        "data": data_points1,
                        "backgroundColor": color1
                    }
                ]
            },
            "options": {
                "title": {
                    "display": True,
                    "text": chartTitle
                },
                "scales": {
                    "xAxes": [
                        {
                            "scaleLabel": {
                                "display": True,
                                "fontColor": '#00000',
                                "fontSize": 20,
                                "fontStyle": "bold",
                                "labelString": xAxisLabel
                            }
                        }
                    ],
                    "yAxes": [
                        {
                            "scaleLabel": {
                                "display": True,
                                "labelString": yAxisLabel,
                                "fontColor": '#00000',
                                "fontSize": 20,
                                "fontStyle": "bold"
                            }
                        }
                    ]
                }
            }
        }

        # If additional datasets are provided, add them to the chart
        if len(datasets) > 1:
            data_points2 = list(map(int, datasets[1].split(',')))
            second_dataset = {
                "label": categoryLabel2,
                "data": data_points2,
                "backgroundColor": color2
            }
            config['data']['datasets'].append(second_dataset)
        
        if len(datasets) > 2:
            data_points3 = list(map(int, datasets[2].split(',')))
            third_dataset = {
                "label": categoryLabel3,
                "data": data_points3,
                "backgroundColor": color3
            }
            config['data']['datasets'].append(third_dataset)
        if len(datasets) > 3:
            data_points4 = list(map(int, datasets[2].split(',')))
            fourth_dataset = {
                "label": categoryLabel4,
                "data": data_points4,
                "backgroundColor": color4
            }
            config['data']['datasets'].append(fourth_dataset)
        # Prepare POST data
        postdata = {
            'chart': json.dumps(config),
            'width': 500,
            'height': 300,
            'backgroundColor': 'transparent',
        }

        # Make POST request to QuickChart
        resp = requests.post('https://quickchart.io/chart/create', json=postdata)
        parsed = json.loads(resp.text)
        print(resp.text)

        # Prepare response
        result = {
            "chart_url": parsed['url'],
            "message": f"Here is the direct link to the chart for Donwload: {parsed['url']},Please ask instructions for customize further or say instructions",
            "message2": f"Here is the direct link to the chart: {parsed['url']}"


}
        print(f"Chart Configuration: {json.dumps(config)}")
        test = "here is the url as well" +  resp.text
        return Response(response=json.dumps(result), status=200, content_type='application/json')
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response(response=f"An error occurred: {e}", status=500)




@app.route("/chart/line/<string:query>", methods=['GET'])
def get_line_chart(query, label1="Data1", label2="Data2"):
    try:
        # Parse the query to get chart parameters
        dataset1, dataset2 = query.split('|')
        label1 = request.args.get('label1', 'Data1')
        label2 = request.args.get('label2', 'Data2')
        data_points1 = list(map(int, dataset1.split(',')))
        data_points2 = list(map(int, dataset2.split(',')))

        # Prepare chart configuration
        config = {
            "type": "line",
            "data": {
                "labels": [str(i) for i in range(1, len(data_points1) + 1)],
                "datasets": [
                    {
                        "label": label1,  # Use the user-provided label
                        "data": data_points1,
                        "fill": False,
                        "borderColor": "blue"
                    },
                    {
                        "label": label2,  # Use the user-provided label
                        "data": data_points2,
                        "fill": False,
                        "borderColor": "green"
                    }
                ]
            }
        }

        # Prepare POST data
        postdata = {
            'chart': json.dumps(config),
            'width': 500,
            'height': 300,
            'backgroundColor': 'transparent',
        }

        # Make POST request to QuickChart
        resp = requests.post('https://quickchart.io/chart/create', json=postdata)
        parsed = json.loads(resp.text)

        # Prepare response
        result = {
            "chart_url": parsed['url']
        }

        return Response(response=json.dumps(result), status=200, content_type='application/json')
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response(response=f"An error occurred: {e}", status=500)
    

@app.route("/instructions", methods=['GET'])
def instructions():
    try:
        text = """
    Welcome to Anychart!

    To generate a bar chart, provide the following parameters:

    - query: Pipe-separated datasets with comma-separated data points. Example: 10,20,30|40,50,60|70,80,90|100,110,120
    - Title (optional): Chart title. Example: Monthly Sales
    - xAxisLabel (optional): Label for the x-axis. Default is 'X-Axis Label'.
    - yAxisLabel (optional): Label for the y-axis. Default is 'Y-Axis Label'.
    - customLabels (optional): Comma-separated string labels for the x-axis. Example: January,February,March
    - categoryLabel1, categoryLabel2, categoryLabel3, categoryLabel4 (optional): Labels for datasets.
    - color1, color2, color3, color4 (optional): Colors for datasets. Default colors are blue, green, red, and red respectively.
    - FontColor (optional): Color for the font. Default is black.

    Provide the parameters in the chat box, and the system will generate a chart for you!
    """
        return Response(response=json.dumps(text), status=200, content_type='application/json')
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response(response=f"An error occurred: {e}", status=500)



@app.route("/chart/pie/<string:query>", methods=['GET'])
def get_pie_chart(query):
    try:
        # Parse the query to get chart parameters (for demonstration, let's assume query is a comma-separated list of numbers)
        data_points = list(map(int, query.split(',')))

        # Prepare chart configuration
        config = {
            "type": "pie",
            "data": {
                "labels": [str(i) for i in range(1, len(data_points) + 1)],
                "datasets": [{
                    "data": data_points
                }]
            }
        }

        # Prepare POST data
        postdata = {
            'chart': json.dumps(config),
            'width': 500,
            'height': 300,
            'backgroundColor': 'transparent',
        }

        # Make POST request to QuickChart
        resp = requests.post('https://quickchart.io/chart/create', json=postdata)
        parsed = json.loads(resp.text)

        # Prepare response
        result = {
            "chart_url": parsed['url']
        }

        return Response(response=json.dumps(result), status=200, content_type='application/json')
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response(response=f"An error occurred: {e}", status=500)

###############################################################################

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
