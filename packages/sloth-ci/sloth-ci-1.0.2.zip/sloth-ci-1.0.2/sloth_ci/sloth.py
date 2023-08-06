﻿from subprocess import Popen, PIPE, TimeoutExpired
from threading import Thread
from os.path import splitext, basename, abspath, join
from time import sleep
from collections import deque
from importlib import import_module

from cherrypy import HTTPError

from slugify import slugify

import logging


class Sloth:
    '''Base Sloth class.

    Each instance represents a separate Sloth app,
    with its own config, log, action queue, and queue processor.

    Each app listens for incoming requests on its own URL path.
    '''

    def __init__(self, config):
        self.config = config

        self.name = slugify(self.config['listen_point'])
        
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        self.processing_logger = self.logger.getChild('processing')
        self.log_handlers = {}

        self.queue = deque()
        self._queue_lock = False

        self.queue_processor = None
        self._processing_lock = False

    @classmethod
    def extend(cls, extensions):
        '''Sequentially chain-inherit Sloth classes from extensions.
    
        The first extension's Sloth class inherits from the base Sloth class and becomes the base class, then the second one inherits from it, and so on.

        :param extensions: list of extensions to load.
    
        :returns: ExtendedSloth is a Sloth class inherited from all extensions' Sloth classes; errors—list of errors raised during the extensions loading.
        '''
    
        ExtendedSloth = cls
        errors = []

        if extensions:
            for extension in extensions:
                try:
                    ext = import_module('.ext.%s' % extensions[extension]['module'], package=__package__)
            
                    ExtendedSloth = ext.extend(ExtendedSloth, extension)

                except Exception as e:
                    errors.append('Could not load extension %s: %s' % (extension, e))

        return ExtendedSloth, errors

    def handle(self, request):
        '''Validate, extract, and process incoming payload.
        
        :param request: a cherrypy.request instance
        '''

        self.logger.debug('Payload received from %s - %s' % (
                request.remote.ip,
                request.headers['User-Agent']
            )
        )

        try:
            provider, provider_data = self.config['provider'].popitem()

            validator = import_module('.validators.%s' % provider, package=__package__)

        except ImportError as e:
            self.logger.critical('No matching validator found: %s' % e)
            raise HTTPError(500, 'No matching validator found: %s' % e)

        validation_data = provider_data or {}

        validation_status, validation_message, validator_params = validator.validate(request, validation_data)

        self.logger.debug(validation_message.format_map(validator_params))

        if validation_status == 200:
            self.logger.info('Valid payload received')
                
        else:
            raise HTTPError(validation_status, validation_message.format_map(validator_params))

        self.process(validator_params)

    def process(self, validator_params):
        '''Queue execution of actions with certain params. 
        
        Params are taken from the ``params`` config section and extracted from the incoming payload.
        
        :param validator_params: params exctacted from the payload
        '''

        params = self.config.get('params', {})

        params.update(validator_params)

        if not self._queue_lock:
            self.queue.append(params)
        
        if not self.queue_processor or not self.queue_processor.is_alive():
            self.queue_processor = Thread(target=self.process_queue, name=self.name)
            self.queue_processor.start()

    def process_queue(self):
        '''Processes execution queue in a separate thread.'''

        actions = self.config.get('actions')

        if actions:
            while self.queue:
                if self._processing_lock:
                    self.processing_logger.warning('Queue processing interrupted')
                    break
                
                params = self.queue.popleft()

                for action in actions:
                    try:
                        self.execute(action.format_map(params))

                    except KeyError as e:
                        self.processing_logger.critical('Unknown param in action: %s', e)

                        if self.config.get('stop_on_first_fail'):
                            break

                    except Exception as e:
                        self.processing_logger.critical('Execution failed: %s', e)

                        if self.config.get('stop_on_first_fail'):
                            break

        self.processing_logger.info('Execution queue is empty')
        return True

    def execute(self, action):
        '''Executes an action in an ordinary Popen.

        :param action: action to be executed

        :returns: True if successful, Exception otherwise
        '''

        self.processing_logger.info('Executing action: %s', action)

        try:
            process = Popen(
                action.split(),
                cwd=self.config.get('work_dir') or '.',
                stdout=PIPE,
                stderr=PIPE)

            stdout, stderr = process.communicate(timeout=self.config.get('exec_timeout'))
            
            self.processing_logger.debug('stdout: %s' % bytes.decode(stdout))
            self.processing_logger.debug('stderr: %s' % bytes.decode(stderr))

            self.processing_logger.info('Finished')
            
            return True

        except TimeoutExpired:
            process.kill()

            stdout, stderr = process.communicate()
            
            self.processing_logger.debug(bytes.decode(stdout))
            self.processing_logger.debug(bytes.decode(stderr))

            raise

        except Exception:
            raise

    def stop(self):
        '''Gracefully stop the queue processor.

        New payloads are not added to the queue, existing actions will be finished.
        '''
        self._queue_lock = True
        self.logger.info('Stopped')

    def kill(self):
        '''Immediately stop processing the queue.'''

        self.stop()

        self._processing_lock = True
        self.logger.warning('Killed')