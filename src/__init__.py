
from run_options.web_app import load_app, parse_parameters

params = parse_parameters('run_options/vocabulary', 'run_options/config.ini')

app = load_app(params, False)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
