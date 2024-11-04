# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Vinícius Frigulha Ribeiro
#    Matrícula: 202201737
#    Turma: CC6N
#    Email: viniciusfrigulha@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        # Verifica se 'x' está fora dos limites (V.F.R.)
        if x < 0:
            x = 0
        elif x >= self.largura:
            x = self.largura - 1
    
        # Verifica se 'y' está fora dos limites (V.F.R.)
        if y < 0:
            y = 0
        elif y >= self.altura:
            y = self.altura - 1
        return self.pixels[y * self.largura + x] # Inclusão do índice 'y * self.largura + x' (AJUSTE - V.F.R.)

    def set_pixel(self, x, y, c):
        self.pixels[y * self.largura + x] = c    # Inclusão do índice 'y * self.largura + x' (AJUSTE - V.F.R.)

    def aplicar_por_pixel(self, func):
        resultado = Imagem.nova(self.largura, self.altura)
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor) # Inverção de 'x' com 'y' e correção da indentação (AJUSTE - V.F.R.)
        return resultado

    def invertida(self):
        """
        Método responsável por fazer a inversão das cores de imagens
        através do cáculo 'i = 255 - o', onde 'i' é o valor do pixel 
        da imagem invertida e 'o' é o pixel da imagem original.
        """
        return self.aplicar_por_pixel(lambda c: 255 - c) # Correção de '266' para '255' (AJUSTE - V.F.R.)
    
    # Método para ajustar os valores dos pixels das imagens (V.F.R.)
    def ajusta_pixel(self):
        """
        Método que garante que os valores dos pixels assumam valores
        entre 0 e 255 incluindo-os.
        """
        for x in range(self.largura):
            for y in range(self.altura):
                valor_pixel = self.get_pixel(x, y)

                # Ajusta os pixels fora do range de 0 a 255
                if valor_pixel > 255:
                    valor_pixel = 255
                elif valor_pixel < 0:
                    valor_pixel = 0
                if isinstance(valor_pixel, float):
                    valor_pixel = round(valor_pixel)  # Arredonda o valor do pixel se for float

                self.set_pixel(x, y, valor_pixel)

    # Método para correlacionar (V.F.R.)
    def correlacao(self, kernel):
        """
        Método que aplica correlações entre a imagem e o kernel,
        gerando uma nova imagem.

        O kernel será sempre uma matriz quadrada com número ímpar de linhas e colunas.
        """
        resultado = Imagem.nova(self.largura, self.altura)
        deslocamento = len(kernel) // 2 # Deslocamento do pixel

        # Percorrendo todos os pixels da imagem (largura x altura)
        for x in range(self.largura):
            for y in range(self.altura):
                
                # Variável que acumula o valor da operação de correlação
                soma = 0
                
                # Aplica o kernel ao redor do pixel atual
                for i in range(len(kernel)):
                    for j in range(len(kernel)):
                        # Coordenadas deslocadas do pixel no kernel em relação ao centro
                        pixel_x = x + j - deslocamento
                        pixel_y = y + i - deslocamento

                        # Multiplica o valor do pixel pelo valor correspondente no kernel
                        soma += self.get_pixel(pixel_x, pixel_y) * kernel[i][j]
                # Define o pixel no resultado com o valor calculado
                resultado.set_pixel(x, y, soma)

        return resultado
    
    def retorna_kernel(self, n):
        """
        Método que retorna um kernel de suavização ('blur')
        de dimensões n x n, aplicando um desfoque uniforme.
        """
        valor_kernel = 1 / (n * n)
        kernel = [[valor_kernel for _ in range(n)] for _ in range(n)]
        return kernel

    def borrada(self, n):
        """
        Método que aplica um efeito de desfoque na imagem.
        """
        resultado = self.correlacao(self.retorna_kernel(n))
        resultado.ajusta_pixel()
        return resultado

    def focada(self, n):
        """
        Método que aplica efeito de nitidez na imagem.
        """
        imagem_borrada = self.borrada(n)  # Aplica o desfoque
        resultado = Imagem.nova(self.largura, self.altura)

        for x in range(self.largura):
            for y in range(self.altura):
                # Calcula o valor da imagem nítida usando a fórmula dada
                valor_nitido = round((2 * self.get_pixel(x, y)) - imagem_borrada.get_pixel(x, y))
                resultado.set_pixel(x, y, valor_nitido)

        resultado.ajusta_pixel()  # Ajusta os valores dos pixels para garantir que estejam entre 0 e 255
        return resultado

    # Método auxiliar para realizar testes do Kernel Ox (V.F.R.)
    def bordas_x(self):
        """
        Método que faz o tratamento horizontal (bordas verticais)
        """
        kernel_x = [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]

        return self.correlacao(kernel_x)

    # Método auxiliar para realizar testes do Kernel Oy (V.F.R.)
    def bordas_y(self):
        """
        Método que faz o tratamento vertical (bordas horizontais)
        """
        kernel_y = [
            [1, 2, 1],
            [0, 0, 0],
            [-1, -2, -1]
        ]

        return self.correlacao(kernel_y)  
    
    # Método que faz o tratamento das bordas de uma imagem (V.F.R.)
    def bordas(self):
        """
        Método que reconhece as bordas de uma imagem.
        """
        # Aplica correlação para as bordas
        bordas_x = self.bordas_x()
        bordas_y = self.bordas_y()

        # Cria a imagem de bordas combinando os resultados
        largura, altura = self.largura, self.altura
        imagem_bordas = Imagem.nova(largura, altura)

        for x in range(largura):
            for y in range(altura):
                # Calcula a magnitude da borda
                magnitude = min(255, math.sqrt(bordas_x.get_pixel(x, y) ** 2 + bordas_y.get_pixel(x, y) ** 2))
                imagem_bordas.set_pixel(x, y, magnitude)
        
        imagem_bordas.ajusta_pixel()  # Ajusta os valores dos pixels da imagem de bordas
        return imagem_bordas

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    
    # QUESTÃO 02 - INVERTER A IMAGEM 'BLUEGILL.PNG' (V.F.R.):
    imagem_original_q2 = Imagem.carregar('test_images/bluegill.png')   # Carregando a imagem original
    imagem_invertida = imagem_original_q2.invertida()                  # Invertendo a imagem
    # imagem_invertida.mostrar()
    imagem_invertida.salvar('results_vini/Q02_bluegill_invertida.png') # Salvando a imagem no path indicado

    # QUESTÃO 04 - APLICAR O KERNEL NA IMAGEM 'PIGBIRD'
    imagem_original_q4 = Imagem.carregar('test_images/pigbird.png')
    kernel_q4 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    imagem_correlacao = imagem_original_q4.correlacao(kernel_q4)
    # imagem_correlacao.mostrar()
    imagem_correlacao.salvar('results_vini/Q04_pigbird_correlacao.png')

    # GERANDO A IMAGEM BORRADA DO 'CAT.PNG'
    imagem_original_borrada = Imagem.carregar('test_images/cat.png')
    imagem_borrada = imagem_original_borrada.borrada(5)
    # imagem_borrada.mostrar()
    imagem_borrada.salvar('results_vini/cat_borrada.png')

    # GERANDO A IMAGEM NÍTIDA DO 'PYTHON.PNG'
    imagem_original_nitida = Imagem.carregar('test_images/python.png')
    imagem_nitida = imagem_original_nitida.focada(11)
    # imagem_nitida.mostrar()
    imagem_nitida.salvar('results_vini/python_nitida.png')

    # QUESTÃO 06 - APLICAR BORDAS DA IMAGEM 'CONSTRUCTOR.PNG'
    imagem_constructor = Imagem.carregar('test_images/constructor.png')
    # imagem_Ox = imagem_constructor.bordas_x()
    # imagem_Oy = imagem_constructor.bordas_y()
    imagem_bordas = imagem_constructor.bordas()
    # imagem_Ox.mostrar()       # Kernel Ox
    # imagem_Oy.mostrar()       # Kernel Oy
    # imagem_bordas.mostrar()   # Bordas Ox e Oy combinadas
    imagem_bordas.salvar('results_vini/constructor_bordas.png')

    
    pass

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
