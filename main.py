import fitz
import re
import os
import json
from typing import List, Dict, Optional

class ExtractorUFRGS:
    def __init__(self, pdf_path: str):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")
        self.doc = fitz.open(pdf_path)
        self.questoes = []
        self.materia_atual = None
        self.imagens_por_pagina = {}
        self.pasta_imagens = "imagens_questoes"
        self._criar_pasta_imagens()
        
    def _criar_pasta_imagens(self):
        """Cria pasta para armazenar imagens"""
        os.makedirs(self.pasta_imagens, exist_ok=True)
        
    def extrair_todas_questoes(self) -> List[Dict]:
        """Extrai todas as questões do vestibular"""
        
        # Primeira passagem: extrair todas as imagens
        self._extrair_todas_imagens()
        
        texto_completo = ""
        
        # Segunda passagem: extrair texto com marcadores de matéria e página
        for page_num in range(len(self.doc)):
            try:
                page = self.doc[page_num]
                texto_pagina = page.get_text("text")
                
                # Detectar matéria
                self._detectar_materia(texto_pagina)
                
                # Adicionar marcador de página
                texto_completo += f"\n[PAGINA:{page_num}]\n"
                
                # Adicionar marcador de matéria
                if self.materia_atual:
                    texto_completo += f"[MATERIA:{self.materia_atual}]\n"
                
                texto_completo += texto_pagina
            except Exception as e:
                print(f"Erro ao processar página {page_num}: {e}")
                continue
        
        # Processar todo o texto de uma vez
        if texto_completo:
            self.questoes = self._processar_texto_completo(texto_completo)
        
        # Filtrar questões vazias
        self.questoes = [q for q in self.questoes if q['enunciado'].strip()]
        
        # Ordenar por número de questão
        self.questoes.sort(key=lambda q: q['numero'])
        
        return self.questoes
    
    def _extrair_todas_imagens(self):
        """Extrai todas as imagens do PDF com seus dados de posição"""
        for page_num in range(len(self.doc)):
            try:
                page = self.doc[page_num]
                image_list = page.get_images()
                
                self.imagens_por_pagina[page_num] = []
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    try:
                        base_image = self.doc.extract_image(xref)
                        rects = page.get_image_rects(xref)
                        
                        # Salvar imagem em arquivo
                        filename = f"pag{page_num}_img{img_index}.{base_image['ext']}"
                        filepath = os.path.join(self.pasta_imagens, filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(base_image["image"])
                        
                        # Armazenar informações da imagem
                        self.imagens_por_pagina[page_num].append({
                            "arquivo": filename,
                            "caminho": filepath,
                            "pagina": page_num,
                            "index": img_index,
                            "bbox": rects[0] if rects else None,
                            "formato": base_image["ext"]
                        })
                        
                        print(f"✓ Imagem extraída: {filename}")
                    except Exception as e:
                        print(f"Erro ao extrair imagem {img_index} da página {page_num}: {e}")
                        continue
                        
            except Exception as e:
                print(f"Erro ao processar imagens da página {page_num}: {e}")
                continue
    
    def _detectar_materia(self, texto: str):
        """Detecta a matéria no texto da página"""
        materias = {
            "PORTUGUÊS": "Português",
            "LITERATURA": "Literatura",
            "MATEMÁTICA": "Matemática",
            "FÍSICA": "Física",
            "QUÍMICA": "Química",
            "HISTÓRIA": "História",
            "GEOGRAFIA": "Geografia",
            "BIOLOGIA": "Biologia",
        }
        
        for keyword, materia in materias.items():
            if re.search(rf'\b{keyword}\b', texto, re.IGNORECASE):
                self.materia_atual = materia
                break
    
    def _processar_texto_completo(self, texto: str) -> List[Dict]:
        """Processa o texto completo e extrai questões - VERSÃO MELHORADA"""
        questoes = []
        
        # Padrão MELHORADO: captura número de questão seguido de ponto e espaço/quebra
        # Usa lookahead para não consumir o próximo número
        padrao_questao = r'\n\s*(\d{1,3})\s*\.\s+(.+?)(?=\n\s*\d{1,3}\s*\.\s+|\Z)'
        
        matches = list(re.finditer(padrao_questao, texto, re.DOTALL))
        
        print(f"✓ {len(matches)} questões encontradas")
        
        for i, match in enumerate(matches):
            numero = int(match.group(1))
            texto_questao = match.group(2).strip()
            
            # Extrair matéria e página do contexto anterior ao número
            inicio_match = match.start()
            contexto_anterior = texto[max(0, inicio_match-500):inicio_match]
            
            materia = self._extrair_materia_contexto(contexto_anterior)
            pagina = self._extrair_pagina_contexto(contexto_anterior)
            
            # Obter o número da próxima questão
            proxima_questao_num = None
            if i + 1 < len(matches):
                proxima_questao_num = int(matches[i + 1].group(1))
            
            if texto_questao and len(texto_questao) > 5: # Reduz limite mínimo
                questao = self._estruturar_questao(
                    numero, 
                    texto_questao, 
                    materia,
                    pagina,
                    proxima_questao_num
                )
                questoes.append(questao)
                print(f"  Questão {numero} extraída ({materia})")
        
        return questoes
    
    def _extrair_materia_contexto(self, contexto: str) -> Optional[str]:
        """Extrai matéria do contexto anterior"""
        materias = {
            "PORTUGUÊS": "Português",
            "LITERATURA": "Literatura",
            "MATEMÁTICA": "Matemática",
            "FÍSICA": "Física",
            "QUÍMICA": "Química",
            "HISTÓRIA": "História",
            "GEOGRAFIA": "Geografia",
            "BIOLOGIA": "Biologia",
        }
        
        # Procura pela matéria mais recente no contexto
        for keyword, materia in materias.items():
            if re.search(rf'\b{keyword}\b', contexto, re.IGNORECASE):
                return materia
        
        return self.materia_atual
    
    def _extrair_pagina_contexto(self, contexto: str) -> Optional[int]:
        """Extrai número da página do contexto"""
        match = re.search(r'\[PAGINA:(\d+)\]', contexto)
        return int(match.group(1)) if match else None
    
    def _estruturar_questao(self, numero: int, texto: str, materia: str, pagina: Optional[int], proxima_questao: Optional[int]) -> Dict:
        """Estrutura uma questão individual"""
        
        enunciado = self._extrair_enunciado(texto)
        alternativas = self._extrair_alternativas(texto)
        tipo = self._classificar_tipo_questao(texto)
        
        # Detectar imagens relacionadas
        imagens_relacionadas = self._encontrar_imagens_por_numero(numero, texto, pagina, proxima_questao)
        tem_imagem = len(imagens_relacionadas) > 0
        
        questao = {
            "numero": numero,
            "materia": materia,
            "instrucao": self._extrair_instrucao(texto),
            "enunciado": enunciado,
            "alternativas": alternativas,
            "tipo": tipo,
            "tem_imagem": tem_imagem,
            "imagens": imagens_relacionadas,
            "formulas": self._extrair_formulas(texto)
        }
        
        return questao
    
    def _encontrar_imagens_por_numero(self, numero_questao: int, texto_questao: str, pagina_atual: Optional[int], proxima_questao: Optional[int]) -> List[Dict]:
        """
        Encontra imagens ENTRE a questão atual e a próxima
        """
        imagens_proximas = []
        
        # 1. Verificar se há referência a imagem no texto
        tem_referencia_imagem = bool(re.search(
            r'figura|imagem|gráfico|tabela|diagrama|ilustração|quadro|mapa|inf|chart',
            texto_questao,
            re.IGNORECASE
        ))
        
        # Se não tem referência, retorna vazio
        if not tem_referencia_imagem:
            return []
        
        # 2. Se tem referência e temos página, procura imagens próximas
        if pagina_atual is not None:
            # Procura na mesma página e páginas seguintes (até a próxima questão)
            for offset in range(0, 5):
                pagina_busca = pagina_atual + offset
                
                if pagina_busca in self.imagens_por_pagina:
                    for img in self.imagens_por_pagina[pagina_busca]:
                        imagens_proximas.append({
                            "arquivo": img["arquivo"],
                            "caminho": img["caminho"],
                            "pagina": img["pagina"],
                            "formato": img["formato"]
                        })
                    
                    # Retorna logo após encontrar primeira página com imagens
                    if imagens_proximas:
                        break
        
        # Retorna no máximo 2 imagens
        return imagens_proximas[:2] if imagens_proximas else []
    
    def _extrair_instrucao(self, texto: str) -> Optional[str]:
        """Extrai instrução se houver"""
        match = re.search(
            r'(?:Instrução|INSTRUÇÃO):\s*(.+?)(?=\n\(|$)',
            texto,
            re.DOTALL
        )
        return match.group(1).strip() if match else None
    
    def _extrair_enunciado(self, texto: str) -> str:
        """Extrai o enunciado principal"""
        texto_limpo = re.sub(
            r'(?:Instrução|INSTRUÇÃO):.*?(?=\n\(|$)',
            '',
            texto,
            flags=re.DOTALL
        )
        
        match = re.search(r'^(.+?)\n\s*\([A-E]\)', texto_limpo, re.DOTALL)
        
        if match:
            enunciado = match.group(1).strip()
            enunciado = re.sub(r'l\.\s*\d+', '', enunciado)
            return enunciado
        
        return texto_limpo.strip()
    
    def _extrair_alternativas(self, texto: str) -> List[Dict]:
        """Extrai alternativas (A) a (E)"""
        alternativas = []
        
        padrao = r'\(([A-E])\)\s*(.+?)(?=\([A-F]\)|$)'
        matches = re.finditer(padrao, texto, re.DOTALL)
        
        for match in matches:
            letra = match.group(1)
            conteudo = match.group(2).strip()
            conteudo = ' '.join(conteudo.split())
            
            if conteudo:
                alternativas.append({
                    "letra": letra,
                    "texto": conteudo
                })
        
        return alternativas
    
    def _classificar_tipo_questao(self, texto: str) -> str:
        """Classifica o tipo da questão"""
        if re.search(r'\([VF]\)', texto):
            return "verdadeiro_falso"
        elif re.search(r'[∫∑∏√±×÷≤≥≠∞]|frac|sqrt|\^', texto):
            return "calculo"
        elif len(texto) > 800:
            return "interpretacao_texto"
        
        return "multipla_escolha"
    
    def _extrair_formulas(self, texto: str) -> List[str]:
        """Extrai fórmulas matemáticas"""
        formulas = []
        patterns = [
            r'\b[a-z]\^[0-9]',
            r'\\frac\{.+?\}\{.+?\}',
            r'\\sqrt\{.+?\}',
            r'∫.+?d[xyz]'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, texto)
            formulas.extend(matches)
        
        return list(set(formulas))
    
    def salvar_json(self, arquivo_saida: str):
        """Salva questões em JSON"""
        try:
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                json.dump(self.questoes, f, ensure_ascii=False, indent=2)
            print(f"\n✓ {len(self.questoes)} questões salvas em {arquivo_saida}")
        except Exception as e:
            print(f"❌ Erro ao salvar JSON: {e}")

# ============ USO ============
if __name__ == "__main__":
    pdf_file = "UFRGS-2025.pdf"
    
    try:
        print(f"Processando {pdf_file}...\n")
        extractor = ExtractorUFRGS(pdf_file)
        questoes = extractor.extrair_todas_questoes()
        
        extractor.salvar_json("questoes_ufrgs_2025.json")
        
        print(f"\n{'='*60}")
        print(f"✓ Total de questões extraídas: {len(questoes)}")
        
        # Contar por matéria
        materias_count = {}
        for q in questoes:
            materia = q['materia']
            materias_count[materia] = materias_count.get(materia, 0) + 1
        
        print(f"\n✓ Questões por disciplina:")
        for materia, count in sorted(materias_count.items()):
            print(f"  - {materia}: {count}")
        
        # Contar questões com imagem
        questoes_com_imagem = [q for q in questoes if q['tem_imagem']]
        print(f"\n✓ Questões com imagens: {len(questoes_com_imagem)}")
        
        # Listar números de questões
        numeros = [q['numero'] for q in questoes]
        print(f"\n✓ Sequência de questões: {min(numeros)} a {max(numeros)}")
        print(f"  Total de números únicos: {len(set(numeros))}")
        
        if questoes:
            print("\n" + "="*60)
            print("Amostra da primeira questão:")
            print("="*60)
            print(json.dumps(questoes[0], ensure_ascii=False, indent=2))
            
    except FileNotFoundError as e:
        print(f"❌ Erro: {e}")
        print(f"Coloque o arquivo 'UFRGS-2025.pdf' na pasta: {os.getcwd()}")
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()