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
#


# Imports
import os
import pset1
import unittest

# Diretório
TEST_DIRECTORY = os.path.dirname(__file__)


# Classe para os testes de imagem:
class TestImagem(unittest.TestCase):
    def test_carregar(self):
        resultado = pset1.Imagem.carregar('test_images/centered_pixel.png')
        esperado = pset1.Imagem(11, 11,
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(resultado, esperado)


# Classe para os testes de inversão:
class TestInvertida(unittest.TestCase):
    def test_invertida_1(self):
        im = pset1.Imagem.carregar('test_images/centered_pixel.png')
        resultado = im.invertida()
        esperado = pset1.Imagem(11, 11,
                                [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255])
        self.assertEqual(resultado,  esperado)

    def test_invertida_2(self):
        # Escreva aqui o seu caso de teste - FEITO (V.F.R.)
        im = pset1.Imagem(4, 1, [29, 89, 136, 200])
        resultado = im.invertida()
        esperado = pset1.Imagem(4, 1, [226, 166, 119, 55])
        self.assertEqual(resultado,  esperado)

    def test_imagens_invertidas(self):
        for nome_arquivo in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=nome_arquivo):
                arquivo_entrada = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % nome_arquivo)
                arquivo_saida = os.path.join(TEST_DIRECTORY, 'test_results', '%s_invert.png' % nome_arquivo)
                resultado = pset1.Imagem.carregar(arquivo_entrada).invertida()
                esperado = pset1.Imagem.carregar(arquivo_saida)
                self.assertEqual(resultado,  esperado)


# Classe para os testes dos filtros:
class TestFiltros(unittest.TestCase):
    def test_borrada(self):
        for tamanho_kernel in (1, 3, 7):
            for nome_arquivo in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=tamanho_kernel, f=nome_arquivo):
                    arquivo_entrada = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % nome_arquivo)
                    arquivo_saida = os.path.join(TEST_DIRECTORY, 'test_results',
                                                 '%s_blur_%02d.png' % (nome_arquivo, tamanho_kernel))
                    imagem_entrada = pset1.Imagem.carregar(arquivo_entrada)
                    imagem_entrada_copia = pset1.Imagem(imagem_entrada.largura, imagem_entrada.altura,
                                                        imagem_entrada.pixels)
                    resultado = imagem_entrada.borrada(tamanho_kernel)
                    esperado = pset1.Imagem.carregar(arquivo_saida)
                    self.assertEqual(imagem_entrada, imagem_entrada_copia,
                                     "Cuidado para não modificar a imagem original!")
                    self.assertEqual(resultado,  esperado)

    def test_focada(self):
        for tamanho_kernel in (1, 3, 9):
            for nome_arquivo in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=tamanho_kernel, f=nome_arquivo):
                    arquivo_entrada = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % nome_arquivo)
                    arquivo_saida = os.path.join(TEST_DIRECTORY, 'test_results',
                                                 '%s_sharp_%02d.png' % (nome_arquivo, tamanho_kernel))
                    imagem_entrada = pset1.Imagem.carregar(arquivo_entrada)
                    imagem_entrada_copia = pset1.Imagem(imagem_entrada.largura, imagem_entrada.altura,
                                                        imagem_entrada.pixels)
                    resultado = imagem_entrada.focada(tamanho_kernel)
                    esperado = pset1.Imagem.carregar(arquivo_saida)
                    self.assertEqual(imagem_entrada, imagem_entrada_copia,
                                     "Cuidado para não modificar a imagem original!")
                    self.assertEqual(resultado,  esperado)

    def test_bordas(self):
        for nome_arquivo in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=nome_arquivo):
                arquivo_entrada = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % nome_arquivo)
                arquivo_saida = os.path.join(TEST_DIRECTORY, 'test_results', '%s_edges.png' % nome_arquivo)
                imagem_entrada = pset1.Imagem.carregar(arquivo_entrada)
                imagem_entrada_copia = pset1.Imagem(imagem_entrada.largura, imagem_entrada.altura,
                                                    imagem_entrada.pixels)
                resultado = imagem_entrada.bordas()
                esperado = pset1.Imagem.carregar(arquivo_saida)
                self.assertEqual(imagem_entrada, imagem_entrada_copia,
                                 "Cuidado para não modificar a imagem original!")
                self.assertEqual(resultado,  esperado)

# Classe para os testes de kernel (V.F.R.):
class TestKernel(unittest.TestCase):
    def test_kernel_identidade(self):
        im = pset1.Imagem.carregar('test_images/centered_pixel.png')
        kernel_identidade = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        resultado = im.correlacao(kernel_identidade)
        esperado = pset1.Imagem(11, 11, 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(resultado, esperado) # A identidade deve retornar a própria imagem
    
    def test_kernel_translacao(self):
        im = pset1.Imagem.carregar('test_images/centered_pixel.png')
        kernel_translacao = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        resultado = im.correlacao(kernel_translacao)
        esperado = pset1.Imagem(11, 11, 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(resultado, esperado) # A translação deve mover 2 pixels para a direita

    def test_kernel_media(self):
        im = pset1.Imagem.carregar('test_images/centered_pixel.png')
        kernel_media = [
            [0.0, 0.2, 0.0],
            [0.2, 0.2, 0.2],
            [0.0, 0.2, 0.0]
        ]
        resultado = im.correlacao(kernel_media)
        esperado = pset1.Imagem(11, 11, 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 51, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 51, 51, 51, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 51, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(resultado, esperado) # A média deve retornar uma região suavizada em torno do pixel analisado

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)

