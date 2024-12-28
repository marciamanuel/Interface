# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLineEdit, QPushButton, QLabel, QMessageBox
)
import re

# Constantes para intervalos permitidos
MIN_ROMAN = 1
MAX_ROMAN = 4999

# Funções auxiliares
def validate_roman(n):
    """Valida se a string é um número romano válido."""
    regex = r"^(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))$"
    if not re.fullmatch(regex, n):
        raise ValueError("Número romano inválido: {}".format(n))

def romanos_para_inteiros(n):
    """Converte números romanos para inteiros."""
    romanos = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    valor_anterior = 0
    for letra in reversed(n):
        valor_atual = romanos[letra]
        if valor_atual < valor_anterior:
            total -= valor_atual
        else:
            total += valor_atual
        valor_anterior = valor_atual
    return total

def inteiros_para_romanos(n):
    """Converte inteiros para números romanos."""
    inteiros = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    resultado = []
    for valor, simbolo in inteiros:
        while n >= valor:
            resultado.append(simbolo)
            n -= valor
    return ''.join(resultado)

# Classe principal da calculadora
class CalculadoraRomanos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Números Romanos")
        self.setGeometry(100, 100, 500, 400)
        self.memoria = []  # Lista para armazenar resultados

        # Layout principal
        self.layout_principal = QVBoxLayout()

        # Campos de entrada
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Digite o primeiro número romano")
        self.layout_principal.addWidget(self.input1)

        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Digite o segundo número romano")
        self.layout_principal.addWidget(self.input2)

        # Botões de operação
        botoes_layout = QHBoxLayout()
        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_adicionar.clicked.connect(self.adicionar)
        botoes_layout.addWidget(self.botao_adicionar)

        self.botao_subtrair = QPushButton("Subtrair")
        self.botao_subtrair.clicked.connect(self.subtrair)
        botoes_layout.addWidget(self.botao_subtrair)

        self.botao_multiplicar = QPushButton("Multiplicar")
        self.botao_multiplicar.clicked.connect(self.multiplicar)
        botoes_layout.addWidget(self.botao_multiplicar)

        self.botao_dividir = QPushButton("Dividir")
        self.botao_dividir.clicked.connect(self.dividir)
        botoes_layout.addWidget(self.botao_dividir)

        self.layout_principal.addLayout(botoes_layout)

        # Campo de resultado
        self.resultado_label = QLabel("Resultado: ")
        self.layout_principal.addWidget(self.resultado_label)

        # Botões de memória e sair
        botoes_memoria_layout = QHBoxLayout()
        self.botao_ver_memoria = QPushButton("Ver Memória")
        self.botao_ver_memoria.clicked.connect(self.ver_memoria)
        botoes_memoria_layout.addWidget(self.botao_ver_memoria)

        self.botao_apagar_memoria = QPushButton("Apagar Último")
        self.botao_apagar_memoria.clicked.connect(self.apagar_memoria)
        botoes_memoria_layout.addWidget(self.botao_apagar_memoria)

        self.botao_sair = QPushButton("Sair")
        self.botao_sair.clicked.connect(self.close)
        botoes_memoria_layout.addWidget(self.botao_sair)

        self.layout_principal.addLayout(botoes_memoria_layout)

        # Configurar o layout principal
        container = QWidget()
        container.setLayout(self.layout_principal)
        self.setCentralWidget(container)

    # Métodos das operações
    def adicionar(self):
        self.realizar_operacao("adicionar")

    def subtrair(self):
        self.realizar_operacao("subtrair")

    def multiplicar(self):
        self.realizar_operacao("multiplicar")

    def dividir(self):
        self.realizar_operacao("dividir")

    def realizar_operacao(self, operacao):
        """Realiza a operação matemática entre dois números romanos."""
        try:
            n1 = self.input1.text().strip()
            n2 = self.input2.text().strip()
            validate_roman(n1)
            validate_roman(n2)
            inteiro1 = romanos_para_inteiros(n1)
            inteiro2 = romanos_para_inteiros(n2)

            if operacao == "adicionar":
                resultado_inteiro = inteiro1 + inteiro2
            elif operacao == "subtrair":
                resultado_inteiro = inteiro1 - inteiro2
            elif operacao == "multiplicar":
                resultado_inteiro = inteiro1 * inteiro2
            elif operacao == "dividir":
                if inteiro2 == 0:
                    raise ZeroDivisionError("Erro: Divisão por zero.")
                resultado_inteiro = inteiro1 // inteiro2
            else:
                raise ValueError("Operação desconhecida.")

            if not (MIN_ROMAN <= resultado_inteiro <= MAX_ROMAN):
                raise ValueError(
                    "Erro: Resultado fora do intervalo permitido ({}-{}).".format(MIN_ROMAN, MAX_ROMAN)
                )

            resultado_romano = inteiros_para_romanos(resultado_inteiro)
            self.memoria.append(resultado_romano)
            self.resultado_label.setText("Resultado: {}".format(resultado_romano))
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    # Métodos de memória
    def ver_memoria(self):
        """Exibe os valores armazenados na memória."""
        if self.memoria:
            QMessageBox.information(self, "Memória", "Memória: " + ", ".join(self.memoria))
        else:
            QMessageBox.information(self, "Memória", "A memória está vazia.")

    def apagar_memoria(self):
        """Apaga o último valor da memória."""
        if self.memoria:
            self.memoria.pop()
            QMessageBox.information(self, "Memória", "Último valor apagado.")
        else:
            QMessageBox.warning(self, "Memória", "A memória já está vazia.")

# Inicialização do aplicativo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = CalculadoraRomanos()
    janela.show()
    sys.exit(app.exec_())
