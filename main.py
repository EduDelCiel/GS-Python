import pandas as pd
import os

class AnalisadorMercadoTrabalho:
    def __init__(self):
        self.dados = {}
        self.paises_disponiveis = []
        self.tags_paises = self.criar_dicionario_tags()
        self.carregar_dados()
    
    def criar_dicionario_tags(self):
        # Mapeia nomes de paises para codigos ISO abreviados
        return {
            'Argentina': '[ARG]',
            'Australia': '[AUS]', 
            'Brazil': '[BRA]',
            'Canada': '[CAN]',
            'Chile': '[CHL]',
            'China': '[CHN]',
            'Cuba': '[CUB]',
            'Germany': '[DEU]',
            'Egypt': '[EGY]',
            'UK': '[GBR]',
            'India': '[IND]',
            'Japan': '[JPN]',
            'South Korea': '[KOR]',
            'Mexico': '[MEX]',
            'Nigeria': '[NGA]',
            'Russia': '[RUS]',
            'Sweden': '[SWE]',
            'USA': '[USA]',
            'South Africa': '[ZAF]'
        }
    
    def carregar_dados(self):
        # Carrega arquivos CSV de dados da pasta 'dados/'
        try:
            self.dados['expectativa_vida'] = pd.read_csv('dados/expectativa_vida.csv')
            self.dados['forca_trabalho'] = pd.read_csv('dados/forca_de_trabalho.csv')
            self.dados['pib'] = pd.read_csv('dados/pib_per_capita.csv')
            self.dados['populacao'] = pd.read_csv('dados/populacao.csv')
            self.dados['setores_economicos'] = pd.read_csv('dados/setores_economicos.csv')
            
            self.paises_disponiveis = self.dados['expectativa_vida']['name'].tolist()
            
            print("OK: TODOS os dados carregados com sucesso!")
            print(f"Paises disponiveis: {len(self.paises_disponiveis)}")
            print("Fontes dos dados:")
            print("- Expectativa de vida: Gapminder")
            print("- Forca de trabalho: OIT/World Bank") 
            print("- PIB per capita: World Bank")
            print("- Populacao: UN Population Division")
            print("- Setores economicos: World Bank")
            
        except Exception as e:
            print(f"ERRO ao carregar dados: {e}")
    
    def get_tag(self, pais):
        # Retorna o codigo ISO abreviado do pais
        return self.tags_paises.get(pais, '[??]')
    
    def _obter_coluna_pais(self, df):
        # Encontra e retorna o nome da coluna que contem os paises
        for col in ['name', 'pais', 'country']:
            if col in df.columns:
                return col
        return 'name'
    
    def _obter_colunas_dados(self, df):
        # Retorna lista de colunas numericas (excluindo geo, name, pais, etc)
        return [col for col in df.columns if col not in ['geo', 'name', 'pais', 'country', 'ano']]

    # =========================================================================
    # FUNCOES OBRIGATORIAS DO TRABALHO
    # =========================================================================

    def apresenta_dado(self, nome_dado):
        # Exibe um dado especifico para todos os paises no ano mais recente
        if nome_dado not in self.dados:
            print(f"Erro: Dado '{nome_dado}' não encontrado!")
            return None
        
        df = self.dados[nome_dado]
        coluna_pais = self._obter_coluna_pais(df)
        colunas_dados = self._obter_colunas_dados(df)
        
        if not colunas_dados:
            print("Nenhuma coluna de dados disponivel")
            return None
        
        ultimo_ano = colunas_dados[-1]
        resultado = {}
        
        for _, row in df.iterrows():
            pais = row[coluna_pais]
            valor = row[ultimo_ano]
            if pd.notna(valor):
                resultado[pais] = valor
        
        print(f"\nDADO: {nome_dado.upper().replace('_', ' ')}")
        print(f"ANO: {ultimo_ano}")
        print("-" * 50)
        
        for pais, valor in resultado.items():
            tag = self.get_tag(pais)
            print(f"{tag} {pais}: {valor}")
        
        return resultado

    def apresenta_pais(self, nome_pais):
        # Exibe todos os dados disponiveis para um pais especifico
        if nome_pais not in self.paises_disponiveis:
            print(f"Erro: País '{nome_pais}' não encontrado!")
            return None
        
        resultado = {}
        tag = self.get_tag(nome_pais)
        
        print(f"\n{tag} {nome_pais} - TODOS OS DADOS DISPONÍVEIS")
        print("=" * 60)
        
        for nome_dado, df in self.dados.items():
            coluna_pais = self._obter_coluna_pais(df)
            
            if nome_pais in df[coluna_pais].values:
                dados_pais = df[df[coluna_pais] == nome_pais]
                colunas_dados = self._obter_colunas_dados(df)
                
                if colunas_dados:
                    ultimo_ano = colunas_dados[-1]
                    if ultimo_ano in dados_pais.columns:
                        valor = dados_pais[ultimo_ano].iloc[0]
                        if pd.notna(valor):
                            resultado[nome_dado] = valor
                            
                            if nome_dado == 'expectativa_vida':
                                print(f"[EXPECTATIVA] Idade: {valor} anos")
                            elif nome_dado == 'forca_trabalho':
                                print(f"[FORCA TRAB] Percentual: {valor}%")
                            elif nome_dado == 'pib':
                                try:
                                    print(f"[PIB] USD: ${float(valor):,.2f}")
                                except Exception:
                                    print(f"[PIB] Valor: {valor}")
                            elif nome_dado == 'populacao':
                                try:
                                    print(f"[POPULACAO] Pessoas: {int(float(valor)):,}")
                                except Exception:
                                    print(f"[POPULACAO] Valor: {valor}")
                            elif nome_dado == 'setores_economicos':
                                print(f"[SETORES] Dados disponiveis")
        
        print("-" * 60)
        return resultado

    def calcula_media(self, nome_dado):
        # Calcula a media aritmética de um dado para todos os paises
        dados = self.apresenta_dado(nome_dado)
        if not dados:
            return None
        
        valores = [v for v in dados.values() if isinstance(v, (int, float)) and pd.notna(v)]
        
        if not valores:
            print("Nenhum valor numérico disponível para cálculo")
            return None
        
        media = sum(valores) / len(valores)
        print(f"\n[MEDIA] {nome_dado}: {media:.2f}")
        print(f"   Paises com dados: {len(valores)}")
        return media

    def calcula_variancia(self, nome_dado):
        # Calcula a variancia e desvio padrao de um dado
        dados = self.apresenta_dado(nome_dado)
        if not dados:
            return None
        
        valores = [v for v in dados.values() if isinstance(v, (int, float)) and pd.notna(v)]
        
        if len(valores) < 2:
            print("Número insuficiente de valores para calcular variância")
            return None
        
        media = sum(valores) / len(valores)
        variancia = sum((x - media) ** 2 for x in valores) / len(valores)
        
        print(f"\n[VARIANCIA] {nome_dado}: {variancia:.2f}")
        print(f"   Desvio Padrao: {variancia ** 0.5:.2f}")
        print(f"   Paises com dados: {len(valores)}")
        return variancia

    def calcula_media_ponderada(self, nome_dado, variavel_peso='populacao'):
        # Calcula media ponderada de um dado usando outro dado como peso
        if nome_dado not in self.dados or variavel_peso not in self.dados:
            print(f"Erro: Dados '{nome_dado}' ou '{variavel_peso}' não encontrados!")
            return None
        
        df_dado = self.dados[nome_dado]
        df_peso = self.dados[variavel_peso]
        
        coluna_pais = self._obter_coluna_pais(df_dado)
        colunas_dados = self._obter_colunas_dados(df_dado)
        colunas_peso = self._obter_colunas_dados(df_peso)
        
        if not colunas_dados or not colunas_peso:
            print("Dados insuficientes para cálculo")
            return None
        
        ultimo_ano_dado = colunas_dados[-1]
        ultimo_ano_peso = colunas_peso[-1]
        
        soma_ponderada = 0
        soma_pesos = 0
        paises_validos = 0
        
        for pais in self.paises_disponiveis:
            if pais in df_dado[coluna_pais].values and pais in df_peso[coluna_pais].values:
                valor_dado = df_dado[df_dado[coluna_pais] == pais][ultimo_ano_dado].iloc[0]
                valor_peso = df_peso[df_peso[coluna_pais] == pais][ultimo_ano_peso].iloc[0]
                
                if pd.notna(valor_dado) and pd.notna(valor_peso) and isinstance(valor_dado, (int, float)) and isinstance(valor_peso, (int, float)):
                    soma_ponderada += valor_dado * valor_peso
                    soma_pesos += valor_peso
                    paises_validos += 1
        
        if soma_pesos == 0:
            print("Não foi possível calcular a média ponderada")
            return None
        
        media_ponderada = soma_ponderada / soma_pesos
        
        print(f"\n[MEDIA PONDERADA] {nome_dado}")
        print(f"   Peso: {variavel_peso}")
        print(f"   Valor: {media_ponderada:.2f}")
        print(f"   Paises com dados: {paises_validos}")
        return media_ponderada

    def calcula_correlacao(self, dado1, dado2):
        # Calcula o coeficiente de correlacao de Pearson entre dois dados
        if dado1 not in self.dados or dado2 not in self.dados:
            print(f"Erro: Dados '{dado1}' ou '{dado2}' não encontrados!")
            return None
        
        df1 = self.dados[dado1]
        df2 = self.dados[dado2]
        
        coluna_pais = self._obter_coluna_pais(df1)
        colunas1 = self._obter_colunas_dados(df1)
        colunas2 = self._obter_colunas_dados(df2)
        
        if not colunas1 or not colunas2:
            print("Dados insuficientes para cálculo de correlação")
            return None
        
        ultimo_ano1 = colunas1[-1]
        ultimo_ano2 = colunas2[-1]
        
        valores1 = []
        valores2 = []
        
        for pais in self.paises_disponiveis:
            if pais in df1[coluna_pais].values and pais in df2[coluna_pais].values:
                val1 = df1[df1[coluna_pais] == pais][ultimo_ano1].iloc[0]
                val2 = df2[df2[coluna_pais] == pais][ultimo_ano2].iloc[0]
                
                if pd.notna(val1) and pd.notna(val2) and isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    valores1.append(val1)
                    valores2.append(val2)
        
        if len(valores1) < 2:
            print("Dados insuficientes para cálculo de correlação")
            return None
        
        # Cálculo da correlação de Pearson
        n = len(valores1)
        soma_x = sum(valores1)
        soma_y = sum(valores2)
        soma_xy = sum(x * y for x, y in zip(valores1, valores2))
        soma_x2 = sum(x ** 2 for x in valores1)
        soma_y2 = sum(y ** 2 for y in valores2)
        
        numerador = n * soma_xy - soma_x * soma_y
        denominador = ((n * soma_x2 - soma_x ** 2) * (n * soma_y2 - soma_y ** 2)) ** 0.5
        
        if denominador == 0:
            correlacao = 0
        else:
            correlacao = numerador / denominador
        
        print(f"\n[CORRELACAO] {dado1} vs {dado2}")
        print(f"   Coeficiente: {correlacao:.3f}")
        
        if abs(correlacao) > 0.7:
            intensidade = "FORTE"
        elif abs(correlacao) > 0.3:
            intensidade = "MODERADA" 
        else:
            intensidade = "FRACA"
        
        if correlacao > 0:
            direcao = "POSITIVA"
        else:
            direcao = "NEGATIVA"
            
        print(f"   {intensidade} correlação {direcao}")
        print(f"   Base: {len(valores1)} países com dados válidos")
        
        return correlacao

    # =========================================================================
    # MENUS INTERATIVOS
    # =========================================================================

    def menu_principal(self):
        # Menu principal interativo do sistema
        while True:
            print("\n" + "="*60)
            print("SISTEMA DE ANALISE DO MERCADO DE TRABALHO")
            print("="*60)
            print("1. Ver dados de um pais especifico")
            print("2. Ver um dado para todos os paises") 
            print("3. Listar todos os paises disponiveis")
            print("4. Ver estatisticas gerais")
            print("5. Funcoes estatisticas avancadas")
            print("0. Sair")
            
            opcao = input("\nEscolha uma opcao (0-5): ").strip()
            
            if opcao == "1":
                self.menu_dados_pais()
            elif opcao == "2":
                self.menu_dados_gerais()
            elif opcao == "3":
                self.listar_paises()
            elif opcao == "4":
                self.menu_estatisticas()
            elif opcao == "5":
                self.menu_estatisticas_avancadas()
            elif opcao == "0":
                print("Saindo do sistema...")
                break
            else:
                print("Opcao invalida! Tente novamente.")

    def menu_estatisticas_avancadas(self):
        # Menu para acessar calculos estatisticos avancados
        while True:
            print("\n" + "="*50)
            print("FUNÇÕES ESTATÍSTICAS AVANÇADAS")
            print("="*50)
            print("1. Calcular média de um dado")
            print("2. Calcular variância de um dado")
            print("3. Calcular média ponderada")
            print("4. Calcular correlação entre dois dados")
            print("5. Voltar ao menu principal")
            
            opcao = input("\nEscolha uma opcao (1-5): ").strip()
            
            if opcao == "1":
                self.selecionar_dado_para_estatistica('media')
            elif opcao == "2":
                self.selecionar_dado_para_estatistica('variancia')
            elif opcao == "3":
                self.selecionar_dados_para_media_ponderada()
            elif opcao == "4":
                self.selecionar_dados_para_correlacao()
            elif opcao == "5":
                break
            else:
                print("Opcao invalida!")

    def selecionar_dado_para_estatistica(self, tipo_estatistica):
        # Menu para escolher um dado e calcular sua estatistica
        print("\nDADOS DISPONIVEIS PARA ANALISE:")
        dados_lista = list(self.dados.keys())
        for i, dado in enumerate(dados_lista, 1):
            print(f"{i}. {dado.replace('_', ' ').title()}")
        
        try:
            opcao = int(input(f"\nEscolha o dado (1-{len(dados_lista)}): "))
            if 1 <= opcao <= len(dados_lista):
                dado_escolhido = dados_lista[opcao - 1]
                
                if tipo_estatistica == 'media':
                    self.calcula_media(dado_escolhido)
                elif tipo_estatistica == 'variancia':
                    self.calcula_variancia(dado_escolhido)
            else:
                print("Opcao invalida!")
        except ValueError:
            print("Por favor, digite um numero valido!")

    def selecionar_dados_para_media_ponderada(self):
        # Menu para escolher dado principal e variavel peso para media ponderada
        print("\nDADOS DISPONIVEIS:")
        dados_lista = list(self.dados.keys())
        for i, dado in enumerate(dados_lista, 1):
            print(f"{i}. {dado.replace('_', ' ').title()}")
        
        try:
            opcao_dado = int(input(f"\nEscolha o dado principal (1-{len(dados_lista)}): "))
            opcao_peso = int(input(f"Escolha a variavel para peso (1-{len(dados_lista)}): "))
            
            if 1 <= opcao_dado <= len(dados_lista) and 1 <= opcao_peso <= len(dados_lista):
                dado_principal = dados_lista[opcao_dado - 1]
                variavel_peso = dados_lista[opcao_peso - 1]
                
                self.calcula_media_ponderada(dado_principal, variavel_peso)
            else:
                print("Opcao invalida!")
        except ValueError:
            print("Por favor, digite numeros validos!")

    def selecionar_dados_para_correlacao(self):
        # Menu para escolher dois dados e calcular correlacao entre eles
        print("\nDADOS DISPONIVEIS:")
        dados_lista = list(self.dados.keys())
        for i, dado in enumerate(dados_lista, 1):
            print(f"{i}. {dado.replace('_', ' ').title()}")
        
        try:
            opcao1 = int(input(f"\nEscolha o primeiro dado (1-{len(dados_lista)}): "))
            opcao2 = int(input(f"Escolha o segundo dado (1-{len(dados_lista)}): "))
            
            if 1 <= opcao1 <= len(dados_lista) and 1 <= opcao2 <= len(dados_lista):
                dado1 = dados_lista[opcao1 - 1]
                dado2 = dados_lista[opcao2 - 1]
                
                self.calcula_correlacao(dado1, dado2)
            else:
                print("Opcao invalida!")
        except ValueError:
            print("Por favor, digite numeros validos!")

    # ... (mantenha suas funções originais listar_paises, menu_dados_pais, 
    # apresenta_pais_interativo, menu_dados_gerais, apresenta_dado_interativo)

    def listar_paises(self):
        # Exibe lista numerada de todos os paises disponiveis
        print(f"\nLISTA DE {len(self.paises_disponiveis)} PAISES DISPONIVEIS:")
        for i, pais in enumerate(self.paises_disponiveis, 1):
            tag = self.get_tag(pais)
            print(f"{i:2d}. {tag} {pais}")

    def menu_dados_pais(self):
        # Menu para selecionar um pais e exibir seus dados
        self.listar_paises()
        
        try:
            num_pais = int(input(f"\nEscolha o numero do pais (1-{len(self.paises_disponiveis)}): "))
            if 1 <= num_pais <= len(self.paises_disponiveis):
                pais_escolhido = self.paises_disponiveis[num_pais - 1]
                self.apresenta_pais(pais_escolhido)
            else:
                print("Numero de pais invalido!")
        except ValueError:
            print("Por favor, digite um numero valido!")

    def menu_dados_gerais(self):
        # Menu para selecionar um dado e exibir para todos os paises
        print("\nDADOS GERAIS PARA TODOS OS PAISES")
        dados_lista = list(self.dados.keys())
        for i, dado in enumerate(dados_lista, 1):
            print(f"{i}. {dado.replace('_', ' ').title()}")
        
        try:
            opcao = int(input(f"\nEscolha o dado (1-{len(dados_lista)}): "))
            if 1 <= opcao <= len(dados_lista):
                dado_escolhido = dados_lista[opcao - 1]
                self.apresenta_dado(dado_escolhido)
            else:
                print("Opcao invalida!")
        except ValueError:
            print("Por favor, digite um numero valido!")

    def menu_estatisticas(self):
        # Menu informativo sobre as funcoes estatisticas disponiveis
        print("\nESTATISTICAS GERAIS")
        print("Use a opção 5 no menu principal para funções estatísticas avançadas")
        print("Inclui: Media, Variancia, Media Ponderada, Correlacao")

# EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    print("INICIANDO SISTEMA DE ANALISE DO MERCADO DE TRABALHO")
    analisador = AnalisadorMercadoTrabalho()
    analisador.menu_principal()