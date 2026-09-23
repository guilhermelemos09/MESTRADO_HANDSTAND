# PROCEDIMENTO OPERACIONAL PADRÃO (POP) – SESSÃO 1
## AVALIAÇÃO DE COMPOSIÇÃO CORPORAL, FORÇA E RESISTÊNCIA ISOMÉTRICA
**Laboratório:** Laboratório de Cineantropometria e Desempenho Humano (LaCiDH) – EEFERP-USP  
**Projeto de Mestrado:** Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk  
**Mestrando:** Guilherme de Paula Lemos | **Orientador:** Prof. Dr. Matheus Machado Gomes  

---

### 1. OBJETIVO GERAL DO POP
Padronizar detalhadamente todas as etapas operacionais da Sessão 1 de coleta de dados no LaCiDH, desde a calibração prévia dos equipamentos, recepção e triagem do voluntário até a execução dos protocolos de bioimpedância tetrapolar, dinamometria isométrica de preensão manual e flexores de punho, teste de 1-RM no shoulder press e teste de resistência em posição invertida (wall-supported handstand). A ordem dos testes e seus intervalos foram rigorosamente desenhados com base em evidências fisiológicas e biomecânicas para mitigar o impacto cumulativo da fadiga sobre a produção de força máxima.

---

### 2. MOMENTO ZERO: RECEPÇÃO E PREPARAÇÃO INICIAL NO LABORATÓRIO
* **2.1 Recepção e Status Documental:** O participante deve comparecer com agendamento oficial prévio e validação ética (TCLE e PAR-Q assinados e validados na Tabela Mestre, conforme o **POP 00 – Recrutamento, Triagem e Consentimento**).
* **2.2 Confirmação Rápida de Elegibilidade:** Prática regular há pelo menos 3 meses de modalidade com Handstand, sustentação livre >= 3s ou >= 3 passadas no HSW, e ausência de lesão articular ativa nos membros superiores nos últimos 12 meses.
* **2.3 Critérios Fisiológicos Pré-Teste:** Ausência de treinos vigorosos nas últimas 48 horas; jejum prévio de 4 horas; ausência de consumo de álcool ou cafeína nas 24 horas antecedentes.
* **2.4 Preparação para Bioimpedância:** Esvaziamento vesical imediato no sanitário; remoção completa de adornos metálicos (relógios, anéis, piercings) e sapatos/meias; uso de vestimenta esportiva leve.
* **2.5 Antropometria Básica:** Aferição da Estatura em estadiômetro de precisão (0,1 cm) e Massa Corporal em balança digital calibrada (0,1 kg), registradas na planilha de campo.

---

### 3. ORDEM PADRONIZADA DOS TESTES E INTERVALOS BIOMECÂNICOS

```mermaid
graph TD
    A["MOMENTO ZERO: Recepção, TCLE, Triagem & Antropometria"] --> B["ETAPA 1: Calibração & Bioimpedância Sanny BIA1011AF (sem fadiga)"]
    B -->|Intervalo 2 min| C["ETAPA 2: Força de Preensão Manual Saehan (3 CVMs bilaterais - 60s int)"]
    C -->|Intervalo 5 min| D["ETAPA 3: Dinamometria Isocinética Flexores de Punho Biodex a 70° (3 CVMs - 60s int)"]
    D -->|Intervalo 5 min| E["ETAPA 4: Teste de 1-RM Shoulder Press (Progressão 10% - 3 min int)"]
    E -->|Intervalo 8 min (Ressíntese PCr)| F["ETAPA 5: Resistência Invertida Wall-Supported HS a 20 cm (2 tentativas - 5 min descanso)"]
```

---

### 4. PROTOCOLO DETALHADO POR ETAPA

#### ETAPA 1: Bioimpedância Elétrica Tetrapolar (Sanny BIA1011AF & BIOSANNY-X)
* **Equipamento:** Bioimpedância Elétrica Tetrapolar AF Sanny, modelo BIA1011AF (Reg. ANVISA: 81540240002).
* **Software de Aquisição:** **BIOSANNY-X** (Software oficial Sanny para análise de composição corporal e bioimpedância tetrapolar).
* **Fundamentação Teórica:** Sun et al. (2003); Kyle et al. (2004); Lukaski et al. (1986); Heyward & Stolarczyk (1996); ACSM (2022/2026); OMS (2020).

**4.1 Padronização da Equação de Predição e Software:**
* **Equação Oficial Adotada:** **`7. Sun et al. (2003)`**
  * *Justificativa Metodológica:* Trata-se da equação de referência internacional desenvolvida a partir de um modelo multicompartimental (4C: hidrodensitometria, diluição com deutério e absorciometria de raios-X de dupla energia - DEXA) e publicada no *American Journal of Clinical Nutrition* (Sun et al., 2003). Por priorizar o índice de condutividade e o volume condutor tecidual ($\text{Estatura}^2 / R$), esta equação é especialmente robusta e fidedigna para populações fisicamente ativas e com maior densidade musculoesquelética de membros superiores e tronco (praticantes de CrossFit®, Calistenia e Ginástica), evitando a superestimação espúria de gordura corporal típica de equações desenvolvidas estritamente na população geral com base no IMC. A mesma equação é rigorosamente padronizada para **100% dos participantes** do estudo, mitigando qualquer viés sistemático nas variáveis preditoras de regressão (`Massa_Livre_Gordura_kg` e `Percentual_Gordura_pct`).

**4.2 Classificação Padronizada do Nível de Atividade Física (BIOSANNY-X):**
No momento do cadastro no software, o avaliador deve questionar a rotina semanal de treinamento dos últimos 3 meses e selecionar rigorosamente conforme os critérios:

| Nível no Software | Critério Operacional Padronizado (Frequência & Duração) | Exemplos Típicos na Amostra |
| :--- | :--- | :--- |
| **Sedentário** | Sem exercício físico programado (< 150 min/sem de atividade leve cotidiana). | Praticante inativo ou destreinado. *(Critério de exclusão se não treinar HS há $\ge 3$ meses).* |
| **Pouco Ativo** | Exercício leve/moderado esporádico (1 a 2x/sem, < 150 min/sem no total). | Prática recreativa irregular ou em retomada recente. |
| **Ativo** | Regular de 3 a 4 sessões/sem (150 a 300 min/sem moderada a vigorosa). | Praticante regular de Calistenia, Ginástica ou CrossFit 3x a 4x/sem (~1h/dia). |
| **Muito Ativo** | **$\ge$ 5 sessões/sem ou $\ge$ 300 a 450 min/sem de intensidade vigorosa.** | Praticantes frequentes (5x/sem, 1h a 1h30/dia) combinando modalidades (CrossFit, Calistenia, Dança, Natação). |
| **Atleta** | Treinamento competitivo sistemático de alto rendimento ($\ge$ 10–15 h/sem). | Ginastas competitivos de elite ou atletas de alto rendimento com periodização estrita e múltiplos turnos diários. |

> [!WARNING]
> **Atenção ao selecionar "Atleta":** Só classifique como "Atleta" participantes que competem em alto rendimento e treinam $\ge 10\text{--}12\text{ h/semana}$. O algoritmo de "Atleta" assume densidade tecidual e hidratação intracelular muito superiores, o que subestimará espuriamente o percentual de gordura se aplicado a praticantes recreacionais (mesmo muito ativos). Para a grande maioria dos voluntários do projeto (que treinam $\ge 5\text{x/sem}$), a classificação correta é **Muito Ativo**.

**4.3 Calibração Diária Prévia (Obrigatória):**
1. Conectar os cabos ao calibrador/resistor padrão de teste de 500 ohms (fornecido pelo fabricante);
2. Abrir o programa **BIOSANNY-X** e executar o módulo de calibração/teste de circuito;
3. O valor de Resistência (R) deve estar estritamente entre 500 ± 2 ohms, e Reatância (Xc) em 0 ± 1 ohm;
4. Confirmada a estabilidade elétrica do circuito, desconectar o calibrador e preparar o voluntário.

**4.4 Procedimento no Participante:**
1. Decúbito dorsal (supino) em maca isolada não condutora;
2. Membros superiores a 30° do tronco e membros inferiores a 45° entre si (sem contato pele com pele);
3. **Repouso passivo imóvel de 5 a 10 minutos** para redistribuição homogênea dos fluidos corporais;
4. Assepsia dos pontos anatômicos com algodão e álcool a 70%;
5. Fixação de 4 eletrodos descartáveis Ag/AgCl no hemicorpo direito (punho e tornozelo, distância intereletrodo de 5 cm);
6. Conectar garras condutoras, preencher os dados antropométricos (Estatura, Massa Corporal, Idade, Sexo), selecionar o **Nível de Atividade Física** (conforme item 4.2) e a equação **`7. Sun et al. (2003)`**, disparando a corrente de 50 kHz;
7. Retenção das variáveis biofísicas brutas (independentes de equação: Resistência $R$, Reatância $Xc$, Ângulo de Fase $AF$) e calculadas (Massa Livre de Gordura em kg, Massa Gorda em kg e % Gordura Corporal);
8. Exportar relatório oficial em PDF gerado pelo **BIOSANNY-X** como `[ID]_sanny.pdf` para a pasta `dados_brutos/`.

---

#### ETAPA 2: Avaliação da Força de Preensão Manual (FPM – Saehan/Jamar)
* **Equipamento:** Dinamômetro hidráulico portátil Saehan SH5001 (equivalente validado ao Jamar®).
* **Fundamentação:** Diretrizes ASHT; Mathiowetz (2002); Roberts et al. (2011); Jaric (2002).
1. Sentado em cadeira sem braços, coluna ereta, pés no solo, ombro aduzido/neutro, **cotovelo flexionado a 90°**, antebraço neutro sem apoio;
2. Manopla na 2ª posição padrão (~4,7 cm de abertura);
3. 3 CVMs de 3 a 5 segundos por membro, alternando Dominante e Não-Dominante;
4. **Intervalo estrito de 60 segundos** entre tentativas no mesmo membro;
5. Comando verbal de incentivo máximo padronizado;
6. Registrar na `PLANILHA_COLETA_CAMPO_LACIDH.xlsx` (o sistema calcula o maior pico em kgf e o índice LSI %).

---

#### ETAPA 3: Pico de Torque Isométrico dos Flexores de Punho (Biodex PRO)
* **Equipamento:** Dinamômetro Isocinético/Isométrico Biodex Multi-Joint System PRO.
* **Fundamentação:** Kerwin & Trewartha (2001); Rohleder & Vogt (2018, 2019); Dvir (2004); Brown (2000); Bishop et al. (2018).
1. Cadeira com encosto a 85°, cintos cruzados peitorais e pélvico;
2. Antebraço posicionado na calha acolchoada em **pronação total**, cotovelo a 90°, imobilizado por cintas de velcro;
3. Alinhamento anatômico-mecânico radiocárpico;
4. Alavanca travada em **70° de extensão funcional de punho** (estratégia de punho do handstand);
5. Calibração automática de gravidade (*Gravity Correction*) e zero anatômico;
6. 1 contração submáxima de familiarização, seguida de 3 CVMs de flexão isométrica de 5 segundos bilaterais;
7. Intervalo de 60 segundos de repouso passivo entre as contrações no mesmo membro;
8. Exportar relatório oficial em PDF como `[ID]_biodex.pdf` para a pasta `dados_brutos/`;
9. **Intervalo obrigatório de 5 minutos de repouso passivo** antes do 1-RM.

---

#### ETAPA 4: Teste de 1 Repetição Máxima (1-RM) no Shoulder Press (SP)
* **Equipamento:** Barra olímpica oficial (FlexFit®, 20kg masc / 15kg fem), anilhas calibradas e travas.
* **Fundamentação:** Haff & Triplett (2021); ACSM (2026); Dias et al. (2005); Soriano et al. (2019); Lemos (2024).
1. Em pé, pés na largura do quadril, glúteos e core ativos, pegada pronada ligeiramente além dos ombros na barra apoiada na clavícula;
2. **Validação Estrita:** Empurrar verticalmente até extensão total dos cotovelos acima da cabeça. Sem push press, sem calcanhares fora e sem hiperextensão lombar;
3. Progressão de carga e protocolo de aquecimento específico:
   * *Aquecimento dinâmico e preparação articular (sem acessórios adicionais):*
     - Mobilidade torácica e de ombros na parede (*wall opener*): 5 respirações profundas empurrando suavemente o tórax em direção ao solo com braços estendidos;
     - Ativação do manguito rotador e estabilizadores escapulares em decúbito ventral no solo (*prone* Y-T-W): 5 repetições controladas em cada formato com polegares voltados ao teto;
     - Ativação do serrátil anterior em prancha alta (*scapular push-up*): 8 a 10 repetições mantendo os cotovelos estendidos;
     - Potenciação com a barra olímpica vazia: 4 a 5 repetições com velocidade máxima na fase concêntrica e pausa de 1 segundo de bloqueio vertical (*lockout*) acima da cabeça;
   * *Estágio 1 (50% PR / 40% massa corporal):* 1 a 2 repetições de adaptação neuromuscular;
   * *Estágios 2 a 5 (60%, 70%, 80%, 90% e 100% da estimativa):* apenas 1 repetição estrita por estágio (potenciação pós-ativação sem indução de fadiga periférica);
   * *Ajuste fino:* redução de 5% se falhar em 100%; acréscimo de 5% se completar facilmente os 100%;
4. **Intervalo obrigatório de 3 minutos de repouso passivo total** entre cada tentativa;
5. Registrar carga máxima absoluta em kg na planilha;
6. **Intervalo pós-teste obrigatório de 8 minutos de repouso passivo total** (ressíntese plena de PCr).

---

#### ETAPA 5: Teste de Resistência em Posição Invertida (Wall-Supported Handstand)
* **Equipamento:** Parede lisa vertical, fita métrica demarcatória no solo, cronômetro centesimal Casio HS-80TW-BU.
* **Fundamentação:** Hedbávný et al. (2013); Sabido et al. (2024); Sands et al. (2016); ACSM (2026).
1. Fita adesiva fixada no solo a exatamente **20 cm da parede**;
2. Posição **Ventre para a Parede (Chest-to-Wall / Belly-to-Wall)** via wall-walk, ponta dos dedos das mãos sobre a linha de 20 cm, corpo alinhado em hollow body, apenas pontas dos dedos dos pés tocando a parede;
3. **Justificativa dos 20 cm:** Assegura alinhamento vertical real de 88° a 90° (>98% do peso sobre os membros superiores), impedindo que o participante descanse o peito na parede ou entre em hiperlordose lombar compensatória ('postura banana');
4. Cronômetro acionado no alinhamento estável e sustentação até a exaustão voluntária máxima;
5. **Critérios de Interrupção:** Cotovelos flexionam > 15°, pés perdem contato com a parede, peito toca na parede ou desistência voluntária;
6. **2 tentativas máximas com 5 minutos de repouso passivo** entre elas. Maior tempo retido em segundos.

---

### 5. EQUAÇÕES AUTOMATIZADAS DE NORMALIZAÇÃO E SIMETRIA
* $1\text{-RM Relativo } (kg/kg) = \text{Carga 1-RM } (kg) / \text{Massa Corporal } (kg)$
* $\text{Pico de Torque Relativo } (N\cdot m/kg) = \text{Pico de Torque no Biodex } (N\cdot m) / \text{Massa Corporal } (kg)$
* $LSI_{FFP} (\%) = (\text{Pico Não-Dominante} / \text{Pico Dominante}) \times 100$
* $\text{Preensão Manual Relativa } (kgf/kg) = \text{FPM Máxima } (kgf) / \text{Massa Corporal } (kg)$
* $LSI_{FPM} (\%) = (\text{FPM Não-Dominante} / \text{FPM Dominante}) \times 100$
* $IMC (kg/m^2) = \text{Massa } (kg) / [\text{Estatura } (m)]^2$

---

### 6. CHECKLIST OPERACIONAL E ROTINA DE PROCESSAMENTO
1. Preencher os dados na planilha `PLANILHA_COLETA_CAMPO_LACIDH.xlsx` (na pasta `dados_brutos/`);
2. Salvar os relatórios oficiais como `[ID]_sanny.pdf` e `[ID]_biodex.pdf` na pasta `dados_brutos/`;
3. Executar o script `calcular_variaveis_forca_lacidh.py` para consolidar a matriz final em `resultados/`;
4. Confirmar o comparecimento do participante para a Sessão 2 no LaBioCoM na data/horário previamente agendados no POP 00 (janela obrigatória de 48h a 7 dias).

---

### 7. REFERÊNCIAS BIBLIOGRÁFICAS COMPLETAS

* **AMERICAN COLLEGE OF SPORTS MEDICINE (ACSM). ** ACSM's Guidelines for Exercise Testing and Prescription. 11th ed. Philadelphia: Wolters Kluwer, 2022/2026.
* **BISHOP, C. et al. ** Interlimb asymmetries: are thresholds a reliable metric for distinguishing between injured and non-injured athletes? The Journal of Strength & Conditioning Research, v. 32, n. 8, p. 2301-2309, 2018. DOI: 10.1519/JSC.0000000000002624.
* **BROWN, L. E. ** Isokinetics in Human Performance. Champaign: Human Kinetics, 2000.
* **DIAS, R. M. R. et al. ** Influência do processo de familiarização para avaliação da força muscular em testes de 1-RM. Revista Brasileira de Medicina do Esporte, v. 11, n. 1, p. 34-38, 2005. DOI: 10.1590/S1517-86922005000100004.
* **DVIR, Z. ** Isocinética: Avaliações Clínicas e Aplicações Terapêuticas. São Paulo: Manole, 2004.
* **GONZALEZ, M. C.; ORLANDI, S. P.; SANTOS, L. P.; BARROS, A. J. D. ** Body composition using bioelectrical impedance: development and validation of a predictive equation for fat-free mass in a middle-income country. Clinical Nutrition, v. 38, n. 5, p. 2175-2179, 2019 (Online 2018). DOI: 10.1016/j.clnu.2018.09.012.
* **HAFF, G. G.; TRIPLETT, N. T. ** Essentials of Strength Training and Conditioning. 4th ed. National Strength and Conditioning Association (NSCA). Champaign: Human Kinetics, 2021.
* **HEDBÁVNÝ, P. et al. ** The relationship between strength abilities and handstand holding time on the floor in artistic gymnastics. Science of Gymnastics Journal, v. 5, n. 3, p. 37-46, 2013.
* **HEYWARD, V. H.; STOLARCZYK, L. M. ** Applied Body Composition Assessment. Champaign: Human Kinetics, 1996.
* **JARIC, S. ** Muscle strength testing: use of normalisation for body size. Sports Medicine, v. 32, n. 10, p. 615-631, 2002. DOI: 10.2165/00007256-200232100-00002.
* **KERWIN, D. G.; TREWARTHA, G. ** Strategies for maintaining a handstand in the anterior-posterior direction. Sports Biomechanics, v. 1, n. 1, p. 79-96, 2001. DOI: 10.1080/14763140108522788.
* **KYLE, U. G. et al. ** Bioelectrical impedance analysis—part I: review of principles and methods. Clinical Nutrition, v. 23, n. 5, p. 1226-1243, 2004. DOI: 10.1016/j.clnu.2004.06.004.
* **LEMOS, G. D. P. ** A força máxima no shoulder press relativa à massa corporal é uma medida preditiva do desempenho no strict handstand push-up em praticantes de CrossFit®. Trabalho de Conclusão de Curso (Graduação em Educação Física e Esporte) – Escola de Educação Física e Esporte de Ribeirão Preto, Universidade de São Paulo, Ribeirão Preto, 2024.
* **LUKASKI, H. C. et al. ** Validation of tetrapolar bioelectrical impedance method to assess human body composition. Journal of Applied Physiology, v. 60, n. 4, p. 1327-1332, 1986. DOI: 10.1152/jappl.1986.60.4.1327.
* **MATHIOWETZ, V. ** Comparison of Rolyan and Jamar dynamometers for measuring grip strength. Occupational Therapy International, v. 9, n. 3, p. 201-209, 2002. DOI: 10.1002/oti.165.
* **ORGANIZAÇÃO MUNDIAL DA SAÚDE (OMS) / WHO. ** Diretrizes da OMS para atividade física e comportamento sedentário: num piscar de olhos. Genebra: World Health Organization, 2020.
* **ROBERTS, H. C. et al. ** A review of the measurement of grip strength in clinical and epidemiological studies: towards a standardised approach. Age and Ageing, v. 40, n. 4, p. 423-429, 2011. DOI: 10.1093/ageing/afr051.
* **ROHLEDER, J.; VOGT, T. ** Wrist strategy in the handstand: An isokinetic and kinematic investigation. Journal of Sports Sciences, v. 36, n. 21, p. 2489-2495, 2018. DOI: 10.1080/02640414.2018.1466986.
* **ROHLEDER, J.; VOGT, T. ** Neuromuscular and mechanical performance factors in the gymnastic handstand. Science of Gymnastics Journal, v. 11, n. 2, p. 187-198, 2019.
* **SABIDO, R. et al. ** Effects of specialized handstand training on shoulder strength, stability, and endurance in athletic populations. Journal of Sports Science & Medicine, v. 23, n. 2, p. 312-321, 2024.
* **SANDS, W. A. et al. ** Static and dynamic posture in gymnastics: A review of balance control and neuromuscular mechanisms. Sports Medicine - Open, v. 2, n. 1, p. 1-14, 2016. DOI: 10.1186/s40798-015-0040-y.
* **SORIANO, M. A. et al. ** The 1-repetition maximum overhead press test: reliability, validity, and relationship with athletic performance. The Journal of Strength & Conditioning Research, v. 33, n. 5, p. 1245-1252, 2019. DOI: 10.1519/JSC.0000000000002998.
* **SUN, S. S.; CHUMLEA, W. C.; HEYMSFIELD, S. B.; LUKASKI, H. C. et al. ** Development of bioelectrical impedance analysis prediction equations for body composition with the use of a multicomponent model for use in epidemiologic surveys. The American Journal of Clinical Nutrition, v. 77, n. 2, p. 331–340, 2003. DOI: 10.1093/ajcn/77.2.331.
