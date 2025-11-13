import pandas as pd
import os

class AnalisadorMercadoTrabalho:
    def __init__(self):
        self.dados = {}
        self.paises_disponiveis = []
        self.tags_paises = self.criar_dicionario_tags()
        self.carregar_dados()
    
    def criar_dicionario_tags(self):
        """Cria dicionário com tags para cada país"""
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
            'South Africa': '[ZAF]',
            'Switzerland': '[CHE]'
        }
    
    def carregar_dados(self):
        """Carrega todos os dados da pasta dados/"""
        try:
            # Carregar CSVs principais
            self.dados['expectativa_vida'] = pd.read_csv('dados/expectativa_vida.csv')
            self.dados['forca_trabalho'] = pd.read_csv('dados/forca_de_trabalho.csv')
            self.dados['pib'] = pd.read_csv('dados/pib_per_capita.csv')
            self.dados['populacao'] = pd.read_csv('dados/populacao.csv')
            self.dados['setores_economicos'] = pd.read_csv('dados/setores_economicos.csv')
            
            # Lista de países disponíveis (usando expectativa de vida como base)
            self.paises_disponiveis = self.dados['expectativa_vida']['name'].tolist()
            
            print("OK: TODOS os dados carregados com sucesso!")
            print(f"Paises disponiveis: {len(self.paises_disponiveis)}")
            
        except Exception as e:
            print(f"ERRO ao carregar dados: {e}")
    
    def get_tag(self, pais):
        """Retorna tag do país ou [??] se não encontrado"""
        return self.tags_paises.get(pais, '[??]')
    
    def menu_principal(self):
        """Menu interativo principal"""
        while True:
            print("\n" + "="*60)
            print("SISTEMA DE ANALISE DO MERCADO DE TRABALHO")
            print("="*60)
            print("1. Ver dados de um pais especifico")
            print("2. Ver um dado para todos os paises") 
            print("3. Listar todos os paises disponiveis")
            print("4. Ver estatisticas gerais")
            print("0. Sair")
            
            opcao = input("\nEscolha uma opcao (0-4): ").strip()
            
            if opcao == "1":
                self.menu_dados_pais()
            elif opcao == "2":
                self.menu_dados_gerais()
            elif opcao == "3":
                self.listar_paises()
            elif opcao == "4":
                self.menu_estatisticas()
            elif opcao == "0":
                print("Saindo do sistema...")
                break
            else:
                print("Opcao invalida! Tente novamente.")
    
    def listar_paises(self):
        """Lista todos os países disponíveis com números e tags"""
        print(f"\nLISTA DE {len(self.paises_disponiveis)} PAISES DISPONIVEIS:")
        for i, pais in enumerate(self.paises_disponiveis, 1):
            tag = self.get_tag(pais)
            print(f"{i:2d}. {tag} {pais}")
    
    def menu_dados_pais(self):
        """Menu para escolher país e dados específicos"""
        self.listar_paises()
        
        try:
            # Escolher país
            num_pais = int(input(f"\nEscolha o numero do pais (1-{len(self.paises_disponiveis)}): "))
            if 1 <= num_pais <= len(self.paises_disponiveis):
                pais_escolhido = self.paises_disponiveis[num_pais - 1]
                tag = self.get_tag(pais_escolhido)
                print(f"\nPais selecionado: {tag} {pais_escolhido}")
                
                # Menu de dados disponíveis
                print("\nDADOS DISPONIVEIS:")
                dados_opcoes = [
                    "Expectativa de Vida", 
                    "Forca de Trabalho", 
                    "PIB per Capita", 
                    "Populacao",
                    "Setores Economicos (Agricultura, Industria, Servicos)"
                ]
                
                for i, dado in enumerate(dados_opcoes, 1):
                    print(f"{i}. {dado}")
                
                opcao_dado = int(input(f"\nEscolha o dado (1-{len(dados_opcoes)}): "))
                
                if 1 <= opcao_dado <= len(dados_opcoes):
                    dados_map = {
                        1: 'expectativa_vida',
                        2: 'forca_trabalho', 
                        3: 'pib',
                        4: 'populacao',
                        5: 'setores_economicos'
                    }
                    
                    dado_escolhido = dados_map[opcao_dado]
                    self.apresenta_pais_interativo(pais_escolhido, dado_escolhido)
                else:
                    print("Opcao de dado invalida!")
            else:
                print("Numero de pais invalido!")
                
        except ValueError:
            print("Por favor, digite um numero valido!")
    
    def apresenta_pais_interativo(self, pais, dado):
        """Mostra dados de um país de forma interativa"""
        tag = self.get_tag(pais)
        print(f"\n{tag} {pais} - {dado.upper().replace('_', ' ')}")
        print("-" * 50)

        if dado in self.dados:
            df = self.dados[dado]

            # Encontrar coluna do país
            coluna_pais = 'name' if 'name' in df.columns else 'pais' if 'pais' in df.columns else 'country'

            if pais in df[coluna_pais].values:
                dados_pais = df[df[coluna_pais] == pais]

                # COLUNAS DISPONÍVEIS (excluindo identificadores)
                colunas_numericas = [col for col in df.columns if col not in ['geo', 'name', 'pais', 'country', 'ano']]

                if colunas_numericas:
                    # Mostrar apenas o RANGE de anos
                    primeiro_ano = colunas_numericas[0]
                    ultimo_ano = colunas_numericas[-1]

                    print(f"PERIODO DISPONIVEL: {primeiro_ano} - {ultimo_ano}")
                    print("-" * 40)

                    try:
                        ano_escolhido = input("Digite o ano que deseja consultar (ex: 2020) ou 'todos': ").strip()

                        if ano_escolhido.lower() != 'todos':
                            # Validar se o ano existe
                            if ano_escolhido in colunas_numericas:
                                if ano_escolhido in dados_pais.columns:
                                    valor = dados_pais[ano_escolhido].iloc[0]
                                    if pd.notna(valor):
                                        print(f"\nDados de {ano_escolhido}:")
                                        print("=" * 40)

                                        if dado == 'setores_economicos':
                                            # Formato especial para setores
                                            try:
                                                agric = dados_pais['agricultura'].iloc[0]
                                                industria = dados_pais['industria'].iloc[0]
                                                servicos = dados_pais['servicos'].iloc[0]
                                                total = agric + industria + servicos

                                                print(f"   Agricultura: {agric:.2f}%")
                                                print(f"   Industria: {industria:.2f}%")
                                                print(f"   Servicos: {servicos:.2f}%")
                                                print(f"   Total: {total:.1f}%")
                                            except Exception:
                                                print("   Erro ao ler colunas de setores economicos")
                                        else:
                                            # Formato padrão para outros dados
                                            print(f"   Valor: {valor}")
                                            if dado == 'expectativa_vida':
                                                print(f"   Idade: {valor} anos")
                                            elif dado == 'pib':
                                                try:
                                                    print(f"   PIB per capita: ${float(valor):,.2f}")
                                                except Exception:
                                                    print(f"   PIB per capita: {valor}")
                                            elif dado == 'populacao':
                                                try:
                                                    print(f"   Populacao: {int(float(valor)):,} pessoas")
                                                except Exception:
                                                    print(f"   Populacao: {valor} pessoas")
                                            elif dado == 'forca_trabalho':
                                                print(f"   Forca de trabalho: {valor}%")
                                    else:
                                        print(f"Nao ha dados para o ano {ano_escolhido}")
                                else:
                                    print(f"Coluna {ano_escolhido} nao encontrada")
                            else:
                                print(f"Ano {ano_escolhido} nao disponivel!")
                                print(f"   Periodo valido: {primeiro_ano} - {ultimo_ano}")

                        else:
                            # Mostrar TODOS os anos de forma organizada
                            print(f"\nEVOLUCAO HISTORICA:")
                            print("=" * 60)

                            if dado == 'setores_economicos':
                                # Tabela especial para setores
                                print(f"{'Ano':<6} {'Agric':<10} {'Indust':<10} {'Servicos':<12} {'Total':<8}")
                                print("-" * 60)

                                if 'ano' in dados_pais.columns:
                                    for _, row in dados_pais.iterrows():
                                        try:
                                            ano = str(int(row['ano']))
                                        except Exception:
                                            ano = str(row.get('ano', ''))
                                        agric = row.get('agricultura', 0) or 0
                                        ind = row.get('industria', 0) or 0
                                        serv = row.get('servicos', 0) or 0
                                        total = agric + ind + serv
                                        print(f"{ano:<6} {agric:<9.1f}% {ind:<9.1f}% {serv:<11.1f}% {total:<7.1f}%")
                                else:
                                    # Mostrar apenas os últimos 10 anos
                                    anos_recentes = colunas_numericas[-10:] if len(colunas_numericas) > 10 else colunas_numericas
                                    for ano in anos_recentes:
                                        try:
                                            agric = dados_pais['agricultura'].iloc[0] if 'agricultura' in dados_pais.columns else 0
                                            ind = dados_pais['industria'].iloc[0] if 'industria' in dados_pais.columns else 0
                                            serv = dados_pais['servicos'].iloc[0] if 'servicos' in dados_pais.columns else 0
                                            total = (agric or 0) + (ind or 0) + (serv or 0)
                                            print(f"{ano:<6} {agric:<9.1f}% {ind:<9.1f}% {serv:<11.1f}% {total:<7.1f}%")
                                        except Exception:
                                            pass
                            else:
                                # Tabela padrão para outros dados - mostrar apenas últimos 15 anos
                                if dado == 'expectativa_vida':
                                    print(f"{'Ano':<8} {'Expectativa':<15}")
                                elif dado == 'pib':
                                    print(f"{'Ano':<8} {'PIB per capita':<20}")
                                elif dado == 'populacao':
                                    print(f"{'Ano':<8} {'Populacao':<20}")
                                elif dado == 'forca_trabalho':
                                    print(f"{'Ano':<8} {'Forca Trabalho':<20}")

                                print("-" * 60)

                                # Mostrar apenas os últimos 15 anos
                                anos_recentes = colunas_numericas[-15:] if len(colunas_numericas) > 15 else colunas_numericas
                                for ano in anos_recentes:
                                    if ano in dados_pais.columns:
                                        valor = dados_pais[ano].iloc[0]
                                        if pd.notna(valor):
                                            if dado == 'expectativa_vida':
                                                print(f"{ano:<8} {valor:<15} anos")
                                            elif dado == 'pib':
                                                try:
                                                    print(f"{ano:<8} ${float(valor):>18,.2f}")
                                                except Exception:
                                                    print(f"{ano:<8} {valor}")
                                            elif dado == 'populacao':
                                                try:
                                                    print(f"{ano:<8} {int(float(valor)):>18,} pessoas")
                                                except Exception:
                                                    print(f"{ano:<8} {valor} pessoas")
                                            elif dado == 'forca_trabalho':
                                                print(f"{ano:<8} {valor:>18}%")

                    except Exception as e:
                        print(f"Erro ao processar: {e}")
                else:
                    print("Nao ha colunas de dados disponiveis")
            else:
                print(f"Pais '{pais}' nao encontrado nos dados de {dado}")
        else:
            print(f"Dado '{dado}' nao encontrado")

    def menu_dados_gerais(self):
        """Menu para ver um dado específico para todos os países"""
        print("\nDADOS GERAIS PARA TODOS OS PAISES")
        dados_opcoes = [
            "Expectativa de Vida", 
            "Forca de Trabalho", 
            "PIB per Capita", 
            "Populacao"
        ]
        
        for i, dado in enumerate(dados_opcoes, 1):
            print(f"{i}. {dado}")
        
        try:
            opcao = int(input(f"\nEscolha o dado (1-{len(dados_opcoes)}): "))
            dados_map = {
                1: 'expectativa_vida',
                2: 'forca_trabalho',
                3: 'pib', 
                4: 'populacao'
            }
            
            if opcao in dados_map:
                self.apresenta_dado_interativo(dados_map[opcao])
            else:
                print("Opcao invalida!")
                
        except ValueError:
            print("Por favor, digite um numero valido!")
    
    def apresenta_dado_interativo(self, dado):
        """Mostra um dado específico para todos os países"""
        print(f"\n{dado.upper().replace('_', ' ')} - TODOS OS PAISES")
        print("-" * 50)
        
        if dado in self.dados:
            df = self.dados[dado]
            
            # Encontrar coluna do país e colunas de dados
            coluna_pais = 'name' if 'name' in df.columns else 'pais' if 'pais' in df.columns else 'country'
            colunas_dados = [col for col in df.columns if col not in ['geo', 'name', 'pais', 'country', 'ano']]
            
            if colunas_dados:
                # Mostrar última coluna disponível (ano mais recente)
                ultima_coluna = colunas_dados[-1]
                print(f"Dados do ano: {ultima_coluna}")
                print("-" * 35)
                
                for _, row in df.iterrows():
                    pais = row[coluna_pais]
                    valor = row[ultima_coluna]
                    tag = self.get_tag(pais)
                    if pd.notna(valor):
                        print(f"{tag} {pais}: {valor}")
            else:
                print("Nao ha colunas de dados disponiveis")
        else:
            print(f"Dado '{dado}' nao encontrado")
    
    def menu_estatisticas(self):
        """Proximo passo"""
        print("\n")
    

# EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    print("INICIANDO SISTEMA DE ANALISE DO MERCADO DE TRABALHO")
    analisador = AnalisadorMercadoTrabalho()
    analisador.menu_principal()