# DICIONÁRIO DE VARIÁVEIS E MAPA DE MODELOS ESTATÍSTICOS (SPSS)
**Projeto de Mestrado:** Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk  
**Mestrando:** Guilherme de Paula Lemos | **Orientador:** Prof. Dr. Matheus Machado Gomes  
**Documento Base:** Projeto de Mestrado - Comitê de Ética (Versão 10/09/2026 Atualizada)

---

### 1. MAPA DOS MODELOS DE REGRESSÃO - HANDSTAND ESTÁTICO (HS)
- **Variável Dependente Principal (Modelos 1 a 5 - Regressão Linear Múltipla):** `HS_Assist_Tempo_Sustentacao_Pico_s` (Melhor tempo de sustentação / Pico em segundos obtido no bloco assistido; retém a maior marca do participante).  
- **Variável Dependente (Modelo 6 - Regressão Logística Binária):** `HS_Livre_Sucesso_Binario` (1 = Sucesso ≥ 3s / 0 = Falha no bloco de entradas livres).

| Modelo | Domínio | Preditores Independentes | Coluna no Dataset | Unidade | Instrumento |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Modelo 1** | **Capacidade Física** | Força Relativa Shoulder Press<br>Resistência Wall-HS<br>Pico de Torque Flexores Punho Relativo (Média Bilateral)<br>Força de Preensão Manual Relativa (Média Bilateral) | `1RM_ShoulderPress_Relativa_kg_kg`<br>`Resistencia_WallHS_Max_s`<br>`FFP_Biodex_Relativo_Media_Nm_kg`<br>`FPM_Relativa_Media_kgf_kg` | kg/kg<br>s<br>N·m/kg<br>kgf/kg | Teste 1-RM SP<br>Wall-HS a 20 cm<br>Biodex PRO a 70°<br>Saehan SH5001 |
| **Modelo 2** | **Controle Postural** | Distância Média CoP-CoM<br>Velocidade Média CoP<br>Entropia Aproximada (ApEn CoP) | `HS_Assist_Distancia_CoP_CoM_Media_mm`<br>`HS_Assist_Velocidade_CoP_mm_s`<br>`HS_Assist_ApEn_CoP` | mm<br>mm/s<br>Adimensional | Bertec (2 placas) + Vicon 3D<br>Bertec (20 Hz)<br>Bertec |
| **Modelo 3** | **Técnica** | Índice de Verticalidade (Ombro-Quadril)<br>Extensão Cervical<br>Flexão Plantar do Tornozelo<br>Largura da Base de Apoio<br>Rotação Externa das Mãos | `HS_Assist_Indice_Verticalidade_deg`<br>`HS_Assist_Extensao_Cervical_deg`<br>`HS_Assist_Flexao_Plantar_deg`<br>`HS_Assist_Base_Apoio_mm`<br>`HS_Assist_Rotacao_Maos_deg` | Graus (°)<br>Graus (°)<br>Graus (°)<br>mm<br>Graus (°) | Vicon 3D<br>Vicon 3D<br>Vicon 3D<br>Vicon 3D<br>Vicon 3D |
| **Modelo 4** | **Antropometria** | Altura do CoM em Inversão<br>Comprimento dos Braços (Alavanca)<br>% Gordura Corporal<br>*(Massa Livre de Gordura)* | `HS_Altura_CoM_mm`<br>`HS_Comprimento_Bracos_mm`<br>`Percentual_Gordura_pct`<br>`Massa_Livre_Gordura_kg` | mm<br>mm<br>%<br>kg | Vicon 3D<br>Vicon 3D<br>Sanny BIA1011-AF<br>Sanny BIA1011-AF |
| **Modelo 5** | **Perfil e Experiência** | Volume de Prática Acumulada Estimada<br>Idade Cronológica | `Volume_Pratica_Acumulada_horas`<br>`Idade_anos` | Horas (h)<br>Anos | Questionário / Forms<br>Questionário / Forms |
| **Modelo 6 (Logístico)** | **Autonomia de Entrada** | Força Relativa Shoulder Press<br>Melhor Tempo de Sustentação no HS Assistido (Pico)<br>Tempo de Treinamento Específico no HS | `1RM_ShoulderPress_Relativa_kg_kg`<br>`HS_Assist_Tempo_Sustentacao_Pico_s`<br>`Tempo_Treino_Especifico_HS_meses` | kg/kg<br>s<br>Meses | Teste 1-RM SP<br>Vicon 3D<br>Questionário / Forms |

---

### 2. MAPA DOS MODELOS DE REGRESSÃO - HANDSTAND WALK DINÂMICO (HSW)
- **Variável Dependente Principal (Modelos 1 a 6 - Regressão Linear Múltipla):** `HSW_Distancia_Percorrida_Mediana_m` (mediana dos trials em metros).

| Modelo | Domínio | Preditores Independentes | Coluna no Dataset | Unidade | Instrumento |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Modelo 1** | **Capacidade Física** | Força Relativa Shoulder Press<br>Resistência Wall-HS<br>Índice de Simetria de Membros nos Flexores de Punho (LSI) | `1RM_ShoulderPress_Relativa_kg_kg`<br>`Resistencia_WallHS_Max_s`<br>`LSI_FFP_pct` | kg/kg<br>s<br>% | Teste 1-RM SP<br>Wall-HS a 20 cm<br>Biodex PRO a 70° |
| **Modelo 2** | **Eficiência da Locomoção** | Variabilidade Espacial de Passada (CV%)<br>Variabilidade Temporal de Passada (CV%)<br>Comprimento Médio de Passada<br>Cadência | `HSW_Variabilidade_Espacial_CV_pct`<br>`HSW_Variabilidade_Temporal_CV_pct`<br>`HSW_Comprimento_Passada_Medio_mm`<br>`HSW_Cadencia_passos_s` | %<br>%<br>mm<br>passos/s | Vicon 3D<br>Vicon 3D<br>Vicon 3D<br>Vicon 3D |
| **Modelo 3** | **Técnica Dinâmica** | Índice de Verticalidade Dinâmico<br>Extensão Cervical<br>Flexão Plantar do Tornozelo<br>Largura da Base de Apoio<br>Rotação Externa das Mãos | `HSW_Indice_Verticalidade_deg`<br>`HSW_Extensao_Cervical_deg`<br>`HSW_Flexao_Plantar_deg`<br>`HSW_Base_Apoio_mm`<br>`HSW_Rotacao_Maos_deg` | Graus (°)<br>Graus (°)<br>Graus (°)<br>mm<br>Graus (°) | Vicon 3D<br>Vicon 3D<br>Vicon 3D<br>Vicon 3D<br>Vicon 3D |
| **Modelo 4** | **Transferência de Habilidade** | Melhor Tempo de Sustentação no HS Estático (Pico)<br>Entropia Aproximada (ApEn) no HS Estático | `HS_Assist_Tempo_Sustentacao_Pico_s`<br>`HS_Assist_ApEn_CoP` | s<br>Adimensional | Vicon 3D<br>Bertec (Plataforma) |
| **Modelo 5** | **Antropometria** | Altura do CoM em Inversão<br>Comprimento dos Braços (Alavanca)<br>% Gordura Corporal<br>*(Massa Livre de Gordura)* | `HS_Altura_CoM_mm`<br>`HS_Comprimento_Bracos_mm`<br>`Percentual_Gordura_pct`<br>`Massa_Livre_Gordura_kg` | mm<br>mm<br>%<br>kg | Vicon 3D<br>Vicon 3D<br>Sanny BIA1011-AF<br>Sanny BIA1011-AF |
| **Modelo 6** | **Perfil e Experiência** | Volume de Prática Acumulada Estimada<br>Idade Cronológica | `Volume_Pratica_Acumulada_horas`<br>`Idade_anos` | Horas (h)<br>Anos | Questionário / Forms<br>Questionário / Forms |

---

### 3. VARIÁVEIS DESCRITIVAS E COMPARAÇÃO ENTRE MODALIDADES (Controle de Multicolinearidade)
*(Estas variáveis foram intencionalmente excluídas dos modelos de regressão do HSW para evitar inflação artificial de variância e multicolinearidade com a cadência e comprimento de passada, sendo reservadas para caracterização do perfil motor de cada modalidade - ex: CrossFit vs. Ginástica):*
- `HSW_Velocidade_Media_m_s`: Velocidade linear média de locomoção invertida (m/s).
- `HSW_Tempo_Contato_Maos_s`: Tempo médio de permanência de cada mão no solo por passada (s).
- `HSW_Tempo_Duplo_Suporte_pct`: Percentual da passada em contato simultâneo de ambas as mãos no solo (%).
- `HS_Livre_Tempo_Max_s`: Tempo máximo atingido em sustentação livre (s).
- `HSW_Distancia_Percorrida_Max_m`: Distância máxima alcançada em um único percurso (m).

---

### 4. NOTA METODOLÓGICA: % GORDURA vs. MASSA LIVRE DE GORDURA NA ANTROPOMETRIA
* **Risco de Colinearidade**: `% Gordura` e `Massa Livre de Gordura` possuem relação matemática direta decorrente da massa corporal.
* **Graus de Liberdade ($N=40$ vs $k=4$)**: Modelos de regressão linear múltipla requerem de 10 a 15 sujeitos por preditor. Com 3 preditores (`Altura_CoM`, `Comp_Bracos`, `%Gordura`), preserva-se o poder estatístico ($1 - \beta \ge 0.80$) e minimiza-se o VIF.
* **Mecânica do Pêndulo Invertido**: O `% Gordura` quantifica diretamente o "lastro inerte" desestabilizador, enquanto a capacidade motora ativa já é avaliada no Modelo 1 (1-RM SP e Biodex). Recomenda-se priorizar o `% Gordura` no modelo inferencial, mantendo a `Massa_Livre_Gordura_kg` no dataset mestre para fins descritivos e comparações de sensibilidade.