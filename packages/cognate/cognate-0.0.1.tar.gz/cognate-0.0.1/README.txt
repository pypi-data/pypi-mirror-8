========
Cognate
========

Welcome to **Cognate**, a package designed with making it easy to create
component services. **Cognate** strives to ease the burden of configuration
management and logging configuration, by providing the infrastructure.
**Cognate** fosters component service architectures by making the design,
implementation, and testing of services less of a chore.

A sample hello world component:

    from cognate.component_core import ComponentCore
    import sys

    class HelloWorld(ComponentCore):
        def __init__(self, name='World', **kwargs):
            self.name = name

            ComponentCore.__init__(self, **kwargs)

        def cognate_options(self, arg_parser):
            arg_parser.add_argument(
                '--name',
                default=self.name,
                help='Whom will receive the salutation.')

        def run(self):
            self.log.info('Hello %s', self.name)


    if __name__ == '__main__':
        argv = sys.argv
        service = HelloWorld(argv=argv)
        service.run()

Allows for the executable:

    $ python hello_world.py -h
    usage: hello_world.py [-h] [--service_name SERVICE_NAME]
                          [--log_level {debug,info,warn,error}]
                          [--log_path LOG_PATH] [--verbose] [--name NAME]

    optional arguments:
      -h, --help            show this help message and exit
      --service_name SERVICE_NAME
                            This will set the name for the current instance.
                            This will be reflected in the log output.
                            (default: HelloWorld)
      --log_level {debug,info,warn,error}
                            Set the log level for the log output. (default: error)
      --log_path LOG_PATH   Set the path for log output. The default file created
                            is "<log_path>/<service_name>.log". If the path
                            ends with a ".log" extension, then the path be a
                            target file. (default: None)
      --verbose             Enable verbose log output to console. Useful for
                            debugging. (default: False)
      --name NAME           Whom will receive the salutation. (default: World)
