import logging
from time import sleep

class PID:
    def __init__(self):
        self.Kp = 0.5   # Ganho Proporcional
        self.Ki = 0.05  # Ganho Integral
        self.Kd = 40.0  # Ganho Derivativo
        self.T = 1.0    # Período de Amostragem (ms)
        self.last_time = 0
        self.referencia = 0.0
        self.erro_total = 0.0
        self.erro_anterior = 0.0
        self.sinal_de_controle = 0.0
        self.sinal_de_controle_MAX = 100.0
        self.sinal_de_controle_MIN = -100.0

    def configura_constantes(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def atualiza_referencia(self, referencia):
        self.referencia = referencia

    def controle(self, saida_medida):
        # logging.debug("Saida Medida: %s", saida_medida)
        # logging.debug("Referencia..: %s", self.referencia)

        erro = self.referencia - saida_medida
        self.erro_total += erro  # Acumula o erro (Termo Integral)

        if self.erro_total >= self.sinal_de_controle_MAX:
            self.erro_total = self.sinal_de_controle_MAX
        elif self.erro_total <= self.sinal_de_controle_MIN:
            self.erro_total = self.sinal_de_controle_MIN

        # Diferença entre os erros (Termo Derivativo)
        delta_error = erro - self.erro_anterior
        sinal_de_controle = self.Kp * erro + (self.Ki * self.T) * self.erro_total + (
            self.Kd / self.T) * delta_error  # PID calcula sinal de controle
        if sinal_de_controle >= self.sinal_de_controle_MAX:
            sinal_de_controle = self.sinal_de_controle_MAX
        elif sinal_de_controle <= self.sinal_de_controle_MIN:
            sinal_de_controle = self.sinal_de_controle_MIN
        self.erro_anterior = erro
        
        return abs(int(sinal_de_controle))


