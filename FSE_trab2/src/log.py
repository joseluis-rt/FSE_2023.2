import logging

def config_logging():
    # Criação do logger
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    # Formato do log
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')

    # Adiciona um manipulador de console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Adiciona um manipulador de arquivo
    file_handler = logging.FileHandler('logfile.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# Exemplo de uso
# configure_logging()

# def example_logging():
#     logging.debug("Esta é uma mensagem de depuração")
#     logging.info('Esta é uma mensagem informativa')
#     logging.warning('Esta é uma mensagem de aviso')
#     logging.error('Esta é uma mensagem de erro')
#     logging.critical('Esta é uma mensagem crítica')

# example_logging()
