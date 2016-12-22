from run_options.web_app import load_app, parse_parameters


if __name__ == '__main__':
    params = parse_parameters('run_options/vocabulary', 'run_options/config.ini')
    app = load_app(params, False)
    app.run(host='0.0.0.0')
