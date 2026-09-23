# PROCEDIMENTO OPERACIONAL PADRÃO (POP) – SESSÃO 2
## CAPTURA CINEMÁTICA 3D (VICON), CINÉTICA (BERTEC) E PIPELINE PYTHON

**Laboratório:** Laboratório de Biomecânica e Controle Motor (LaBioCoM) – EEFERP-USP  
**Projeto de Mestrado:** Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk  
**Mestrando:** Guilherme de Paula Lemos | **Orientador:** Prof. Dr. Matheus Machado Gomes  

---

### 1. OBJETIVO GERAL DO POP
Padronizar minuciosamente todas as etapas operacionais e laboratoriais da **Sessão 2 (LaBioCoM)**:
1. Inicialização, estabilização térmica e calibração óptica/cinética do sistema Vicon Nexus e da plataforma Bertec;
2. Aferição antropométrica manual (9 medidas bilaterais do modelo Plug-in Gait);
3. Instrumentação com marcadores retrorreflexivos (modelo Plug-in Gait modificado com **marcador escapular RBAK**, cluster dorsal antioclusão e marcador do avaliador `M_PESQ`);
4. Condução do aquecimento neuromuscular padronizado com exercícios específicos para punhos, escápulas, core e inversão;
5. Execução dos blocos de equilíbrio estático (**Handstand Assistido e Livre**) e locomoção dinâmica (**Handstand Walk**);
6. Pós-processamento automatizado em Python (filtragem, reconstrução SVD de ombros ocluídos, detecção de eventos e consolidação das variáveis biomecânicas).

---

### 2. MOMENTO ZERO: CRITÉRIOS PRÉVIOS E PREPARAÇÃO DO PARTICIPANTE

* **2.1 Janela Inter-Sessões:** Realizada obrigatoriamente entre **48 horas e 7 dias** após a Sessão 1 (LaCiDH), garantindo recuperação muscular plena sem perda de condicionamento.
* **2.2 Descanso Prévio & Recuperação:** Ausência de treinamento físico vigoroso nas 48 horas antecedentes que induza fadiga residual nos membros superiores, cintura escapular ou tronco.
* **2.3 Vestimenta Obrigatória & Cabelos:** Roupas esportivas de compressão justas (top esportivo / shorts curto de lycra) para permitir a fixação estável dos marcadores sobre os marcos ósseos e mitigar artefatos de tecidos moles (*Soft Tissue Artifacts* - STA). Cabelos longos devem ser rigidamente presos em **coque alto** para desobstruir os marcadores da cabeça e da coluna cervical.
* **2.4 Preparação da Pele:** Palpação dos marcos anatômicos e assepsia prévia com gaze embebida em álcool a 70% para garantir aderência ideal da fita adesiva dupla-face.

---

### 3. CRONOGRAMA E FLUXOGRAMA DOS TESTES

```mermaid
graph TD
    A["01. Inicialização & Estabilização Térmica Vicon (30 min)"] --> B["02. Calibração Vicon (< 0.20 mm) & Zero Bertec"]
    B --> C["03. Antropometria Manual (9 Medidas) & Instrumentação"]
    C --> D["04. Captura Estática de Calibração Cal.c3d (3s)"]
    D --> E["05. Aquecimento Específico Padronizado (4-5 min)"]
    E --> F["06. Handstand Assistido (até 3 tent. | 90s int.)"]
    F -->|Intervalo 3 min| G["07. Handstand Livre (3 tent. | 90s int.)"]
    G -->|Intervalo 10 min (Recuperação PCr)| H["08. Handstand Walk Dinâmico (3 tent. válidas | 90s int.)"]
    H --> I["09. Pipeline Automatizado Python (Limpeza, SVD & Métricas)"]
    I --> J["10. Consolidação Final Dataset Mestrado (SPSS Ready)"]
```

| Etapa | Procedimento / Bloco | Duração / Tentativas | Intervalo de Repouso |
| :--- | :--- | :---: | :--- |
| **Setup** | Warm-up eletrônico do Vicon + Antropometria manual | 30 minutos contínuos | — |
| **Calibração** | Varinha Vicon + Zero Bertec + Ensaio Estático (`Cal.c3d`) | ~5 minutos | — |
| **Aquecimento** | Mobilidade em pé, prancha alta, pike e ativação na parede (zero chão) | 4 a 5 minutos | Imediato ao teste |
| **HS Assistido** | Subidas guiadas com desmame tátil de 2s (Critério de parada por desempenho: liberado se ≥ 30s e relatar marca máxima) | Até 3 tentativas (retém Melhor Tempo e registra Tentativa do Pico) | 90 segundos entre tent. |
| **Transição** | Repouso passivo sentado + Hidratação livre | 3 minutos | — |
| **HS Livre** | Subidas autônomas sobre a plataforma (3 tentativas obrigatórias para taxa de sucesso; sustentação de ≥ 3s sem exigir exaustão em todas) | 3 tentativas (registra Taxa de Acertos e Tentativa do Pico) | 90 segundos entre tent. |
| **Transição** | Repouso passivo completo (recuperação de PCr e sistema vestibular) | **10 minutos** | — |
| **HSW Dinâmico** | Marcha na pista instrumentada (até 3 entradas por tentativa; mínimo 3 passos para validar; desfecho: mediana) | **3 tentativas válidas** | 90 segundos entre tent. |
| **Pós-Coleta** | Pipeline Python e exportação das matrizes de variáveis | ~5 minutos | Conclusão |

---

### 4. CONFIGURAÇÃO DO SISTEMA, ANTROPOMETRIA E MAPA DE MARCADORES

#### 4.1 Checklist de Inicialização e Estabilização Térmica (Rotina Oficial LaBioCoM)
Para evitar falhas de comunicação de rede, sincronismo e deriva térmica (*thermal drift*), siga a sequência rigorosa:

1. **Ligar o Ar-Condicionado a 19 °C:** O termostato deve ser mantido em 19 °C ininterruptamente para estabilidade eletrônica e óptica das câmeras.
2. **Ligar a Unidade MX Giganet:** Acionar a chave no painel traseiro (sincronizador central de hardware).
3. **Ligar o Switch de Rede PoE+:** Acionar o switch Gigabit Ethernet das câmeras.
4. **Ligar o Computador de Aquisição:** Ligar a CPU dedicada ao Vicon Nexus.
5. **Ligar a TV / Monitor de Retorno:** Ligar a televisão e selecionar a entrada **HDMI 3**.
6. **Abrir o Vicon Nexus:** No painel lateral esquerdo (*System*), confirmar se todas as câmeras (1 Vantage + 8 MX-T40S) apresentam **círculos verdes** operacionais.
7. **Estabilização Térmica Obrigatória (30 minutos):**
   * As câmeras ópticas exigem 30 minutos após serem energizadas para estabilização de sua temperatura interna de operação.
   * **Proibido calibrar a frio:** A dilatação micrométrica das lentes faz com que as câmeras reconstruam marcadores em posições oscilantes (*thermal drift*), degradando a precisão submilimétrica.
   * **Ações simultâneas da equipe durante os 30 min:** Recepção do voluntário, conferência de prontidão, colocação da roupa de compressão, fixação de cabelo em coque alto, assepsia com álcool a 70% e **aferição antropométrica manual das 9 medidas**.

#### 4.2 Calibração Óptica e Cinética
Após os 30 minutos de estabilização térmica:
1. **Mascaramento de Reflexos Parasitas (`Mask Cameras`):** Acionar `Mask Cameras` (`All Cameras`) por 5 segundos para isolar reflexos espúrios de parafusos e piso.
2. **Calibração Dinâmica do Volume (`Wand Calibration`):**
   * Movimentar a varinha em T em trajetórias em "8" contínuas cobrindo todo o volume 3D (do chão até a altura máxima dos pés na vertical);
   * Acumular ~3.500 frames válidos avistados por múltiplas câmeras simultaneamente;
   * **Critério de Aceitação:** Erro residual médio de calibração **< 0,20 mm** (limite máximo de tolerância do laboratório < 0,30 mm).
3. **Origem Global do Sistema (`Set Volume Origin`):**
   * Posicionar o gabarito em L nivelado sobre a plataforma Bertec;
   * Convenção oficial dos eixos: **X = Médio-Lateral**, **Y = Ântero-Posterior** (sentido da marcha) e **Z = Vertical absoluto** (apontando para cima).
4. **Zero da Bertec & Sincronização:** Zerar os canais analógicos da plataforma com o piso descarregado. Frequências: **Cinemática a 100 Hz** e **Bertec a 1.000 Hz**, sincronizados via hardware.

#### 4.3 Protocolo de Aferição Antropométrica Manual (9 Medidas Vicon Plug-in Gait)
Todas as grandezas devem ser aferidas bilateralmente em **milímetros (mm)** com paquímetro antropométrico ou fita métrica inextensível e digitadas na planilha de campo e no formulário de sujeito do Nexus:

| # | Variável na Planilha | Marco Anatômico & Posicionamento | Instrumento | Função no Modelo Cinemático |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `Ombro_Offset_D/E_mm` | Distância vertical da borda superior do acrômio ao sulco bicipital / tubérculo maior | Paquímetro | Centro articular da glenoumeral |
| **2** | `Cotovelo_Largura_D/E_mm` | Diâmetro biepicondilar do úmero (comprimir tecidos moles firmemente) | Paquímetro | Eixo de flexo-extensão do cotovelo |
| **3** | `Punho_Largura_D/E_mm` | Distância entre os processos estilóides do rádio e da ulna | Paquímetro | Centro articular do punho no plano coronal |
| **4** | `Mao_Espessura_D/E_mm` | Espessura dorso-palmar na cabeça do 3º metacarpo | Paquímetro | Distância da superfície de apoio ao marcador dorsal |
| **5** | `Joelho_Largura_D/E_mm` | Diâmetro bicondilar femoral (côndilo medial e lateral do fêmur) | Paquímetro | Centro articular do joelho |
| **6** | `Tornozelo_Largura_D/E_mm` | Diâmetro bimaleolar (maléolo medial da tíbia ao maléolo lateral da fíbula) | Paquímetro | Eixo de rotação talocrural |
| **7** | `Comp_Real_MMII_EIAS_D/E_mm` | Espinha Ilíaca Ântero-Superior (EIAS) até o maléolo medial da tíbia | Fita Métrica | Escalonamento do membro inferior (*Leg Length*) |
| **8** | `Comp_Membro_Trocanter_D/E_mm` | Trocânter maior do fêmur até o maléolo lateral da fíbula | Fita Métrica | Controle e validação anatômica lateral |
| **9** | `Comp_Braco_Acromio_Dedo3_D/E_mm`| Ângulo póstero-lateral do acrômio até a polpa distal do 3º dedo | Fita Métrica | Escalonamento do membro superior (*Arm Length*) |

#### 4.4 Posicionamento dos Marcadores Retrorreflexivos (42 Marcadores)
Utiliza-se o modelo Plug-in Gait modificado com adaptações para a postura invertida, incorporando o **marcador escapular RBAK**, o **cluster dorsal antioclusão** e o **marcador do avaliador `M_PESQ`**:

| Segmento | Rótulos (Labels) | Quant. | Localização Anatômica Exata | Função Biomecânica / Notas |
| :--- | :--- | :---: | :--- | :--- |
| **Cabeça** | `LFHD`, `RFHD`, `LBHD`, `RBHD` | 4 | Têmporas frontais D/E e occipitais D/E em faixa elástica | Orientação cefálica e ângulo cervical |
| **Tronco & Cluster Dorsal** | `C7` | 1 | Processo espinhoso da 7ª vértebra cervical | Segmento torácico e base cervical |
| | `T10` | 1 | Processo espinhoso da 10ª vértebra torácica | Centro torácico e cluster dorsal |
| | **`RBAK`** | 1 | **Ângulo inferior da escápula direita** | **Assimetria tridimensional do tronco no Plug-in Gait (orientação AP e torção)** |
| | `LREF` *(ou `referencia1`)* | 1 | 5 cm à esquerda do processo espinhoso de T10 | Âncora lateral esquerda do cluster dorsal SVD |
| | `RREF` *(ou `referencia2`)* | 1 | 5 cm à direita do processo espinhoso de T10 | Âncora lateral direita do cluster dorsal SVD |
| | `STRN` | 1 | Processo xifoide do esterno | Referência anterior do tronco (*CLAV foi suprimido p/ evitar artefato respiratório*) |
| **Membros Superiores** | `LSHO`, `RSHO` | 2 | Articulação acromioclavicular (ápice do acrômio) | Reconstruídos via SVD caso ocluídos na inversão |
| | `LUPA`, `RUPA` | 2 | Face lateral do braço (terço médio) | Eixo de rotação umeral |
| | `LELB`, `RELB` | 2 | Epicôndilos laterais do úmero | Centro articular do cotovelo |
| | `LFRA`, `RFRA` | 2 | Face lateral do antebraço (terço médio) | Orientação do antebraço (*ou LFRM/RFRM*) |
| | `LWRA`, `RWRA` | 2 | Processo estiloide do rádio | Eixo de flexo-extensão do punho |
| | `LWRB`, `RWRB` | 2 | Processo estiloide da ulna | Eixo de desvio rádio-ulnar do punho |
| | `LFIN`, `RFIN` | 2 | Dorso da mão sobre a base do 3º metacarpo | Detecção de lift-off e touchdown no solo |
| **Pelve** | `LASI`, `RASI` | 2 | Espinhas ilíacas ântero-superiores | Orientação e inclinação pélvica |
| | `LPSI`, `RPSI` | 2 | Espinhas ilíacas póstero-superiores | Centro e nivelamento pélvico |
| **Membros Inferiores** | `LTHI`, `RTHI` | 2 | Face lateral da coxa (terço médio) | Orientação do segmento coxa |
| | `LKNE`, `RKNE` | 2 | Epicôndilos laterais do fêmur | Eixo funcional do joelho |
| | `LTIB`, `RTIB` | 2 | Face lateral da perna (terço médio) | Orientação da tíbia |
| | `LANK`, `RANK` | 2 | Maléolos laterais da fíbula | Eixo articular talocrural |
| | `LHEE`, `RHEE` | 2 | Face posterior do calcâneo na altura dos maléolos | Identificação da verticalidade dos calcanhares |
| | `LTOE`, `RTOE` | 2 | Face dorsal do pé sobre a cabeça do 2º metatarso | Ponta distal e orientação do pé |
| **Marcador do Avaliador** | `Apoio` *(ou `M_PESQ`)* | 1 | **Dorso da mão dominante do pesquisador avaliador** | **Permite ao Python detectar o instante exato de desmame tátil no HS assistido** |

* **Função Mandatória do RBAK:** O modelo biomecânico Plug-in Gait exige um marcador assimétrico posterior no tronco (**RBAK**) para calcular os ângulos tridimensionais da coluna e determinar a orientação ântero-posterior do tórax. Sem o `RBAK`, o software inverte eixos anatômicos e compromete a orientação tridimensional do tronco.

#### 4.5 Captura Estática de Calibração (`[ID]_cal.c3d`)
* **Procedimento:** Voluntário no centro da plataforma Bertec na posição anatômica neutra em pé (braços abduzidos a ~30°, pés paralelos na largura do quadril, olhar fixo no horizonte). Gravação de **3 segundos ininterruptos**.
* **Nomenclatura Obrigatória:** `[ID]_cal.c3d` (ex: `P001_cal.c3d`).
* **Finalidade no Pipeline:** Ensaio mestre de referência anatômica a partir do qual o algoritmo SVD extrai as coordenadas relativas dos ombros (`LSHO`/`RSHO`) em relação ao cluster dorsal (`C7`, `T10`, `LREF`/`RREF`) para a reconstrução rígida em caso de oclusão.

---

### 5. PROTOCOLOS DE EXECUÇÃO DOS TESTES

#### 5.1 Aquecimento Específico Padronizado para Posição Invertida (4 a 5 Minutos – Zero Contato de Tronco no Solo)
Executado imediatamente após a captura estática com o participante já instrumentado. Para preservar a integridade física e o posicionamento anatômico dos 42 marcadores ópticos (especialmente os marcadores da pelve, do esterno e do cluster dorsal), este protocolo elimina qualquer posição de decúbito dorsal ou ventral no solo, preparando o sistema neuromuscular e a propriocepção dos punhos de forma rápida e segura:

| Fase (Tempo) | Exercício Padronizado | Volume / Duração | Foco Biomecânico & Alvo | Técnica de Execução & Pontos de Atenção |
| :--- | :--- | :---: | :--- | :--- |
| **Fase 1 (0 a 1,5 min)**<br>Punhos e Ombros em Pé | **1. Circundução de Punhos em Pé** | 1 minuto (30s cada sentido) | Lubrificação sinovial articular rádio-cárpica e médio-cárpica | Mãos entrelaçadas em pé, movimentos circulares lentos em amplitude máxima sem desconforto. |
| | **2. Abertura Torácica e de Ombros na Parede (*Wall Opener*)** | 5 respirações profundas (~30s) | Mobilidade em flexão pura de ombro e extensão da coluna torácica | Palmas apoiadas na parede na altura dos ombros, pés recuados; afundar suavemente o peito em direção ao chão mantendo braços estendidos. |
| | **3. Sobrecarga Palmar em 4 Apoios (*Rocking* Suave)** | 10 a 12 repetições dinâmicas | Adaptação funcional dos flexores e tolerância à carga em 70° a 90° | Apenas joelhos e mãos no solo (tronco suspenso no ar); deslocar o peso para frente sobre os punhos mantendo cotovelos estendidos. |
| **Fase 2 (1,5 a 3 min)**<br>Cintura Escapular & Apoio Unilateral | **4. Flexões Escapulares em Prancha Alta (*Scapular Push-ups*)** | 1 série de 8 a 10 repetições | Ativação do serrátil anterior e rotação superior da escápula | Prancha alta com cotovelos 100% estendidos (apenas mãos e pés no solo, sem encostar o corpo); realizar protração e retração escapular controlada. |
| | **5. Toques no Ombro em V Invertido (*Shoulder Taps* em *Pike*)** | 10 toques totais (5 cada lado) | Ativação estabilizadora em apoio unimanual transitório (específico para HSW) | Quadril elevado em formato de V invertido com braços alinhados ao tronco; retirar uma mão do solo e tocar o ombro contralateral de forma estável e ritmada. |
| **Fase 3 (3 a 5 min)**<br>Inversão & Estratégia de Punho | **6. Subida Curta de Frente para a Parede (*Belly-to-Wall*)** | 1 subida de 5 a 8 segundos | Acomodação da pressão intracraniana e bloqueio escapular em inversão | Subir escalando os pés pela parede até alinhamento próximo (~30-40 cm); empurrar o solo ativamente pelos ombros e descer com controle. |
| | **7. Subida de Costas com Micro-Solturas (*Back-to-Wall* com Assistência)** | 1 subida com 3 micro-solturas (2 a 3s cada) | Calibração proprioceptiva da estratégia de punho (*wrist strategy*) e dedos em garra | Subir de costas para a parede; o avaliador auxilia o participante a afastar os calcanhares da parede por 2 a 3 segundos (3 vezes consecutivas), instruindo o atleta a pressionar ativamente a ponta dos dedos contra o solo para frear o desequilíbrio. |

---

#### 5.2 Handstand Estático (HS) – Plataforma Bertec
O atleta posiciona as duas mãos inteiramente contidas dentro dos limites físicos da plataforma Bertec, utilizando a distância e o ângulo de abertura (*toe-out*) de sua preferência natural.

##### Bloco 1: Entradas Assistidas (Até 3 Tentativas | 90s Repouso | Critério do Melhor Tempo)
1. **Execução:** O atleta sobe de forma guiada enquanto o avaliador segura suavemente suas pernas pelo terço distal (canelas/tornozelos).
2. **Desmame Tátil:** O avaliador posiciona os calcanhares na vertical absoluta e realiza um **desmame progressivo de contato (*fade-out* tátil) de ~2 segundos**, aliviando a pegada até soltar totalmente as pernas e vocalizar o comando *"SOLTEI"*, recuando as mãos.
3. **Sustentação e Desfecho (Melhor Tempo):** O atleta sustenta a parada de mãos até a perda voluntária de equilíbrio ou contato dos pés com o solo. Para as análises estatísticas dos modelos preditivos do HS, é retido o **Melhor Tempo de Sustentação** (maior duração em segundos entre as tentativas válidas), evitando a penalização por desajustes pontuais ou o viés de fadiga acumulada.
4. **Regra de Parada por Desempenho (*Stopping Rule* - Prevenção de Fadiga para o HSW):**
   * O atleta executa a 1ª tentativa buscando expressar sua capacidade máxima.
   * **Critério de Liberação:** Se o participante atingir **$\ge 30\text{ s}$** e relatar voluntariamente que já atingiu sua marca representativa máxima em uma tentativa válida, **ele é liberado das tentativas subsequentes** para descansar e se poupar para o Handstand Walk (HSW), prevenindo a fadiga neuromuscular precoce da cintura escapular e punhos.
   * **Sem Teto de Tempo:** Destaca-se que **não há estipulação de teto de corte** durante a tentativa (o atleta pode permanecer sustentando pelo tempo que for capaz durante a sua execução).
   * **Tentativas Adicionais:** Novas tentativas (até o limite de 3) serão realizadas apenas se houver queda prematura (por desajuste na subida ou na soltura) ou se o participante julgar ter plenas condições de superar a marca anterior.
5. **Validação na Planilha:** Preencher `OK` na coluna `HS_Assist_T[1-3]_Status`. Caso haja erro na soltura ou desabamento prematuro, marcar `Repetir`. Se o participante for liberado pela regra de parada (ex: atingiu $\ge 30$ s e relatou marca máxima na T1 ou T2), registrar `Dispensado (Critério ≥30s e Marca Máxima)` nas tentativas restantes. Se houver alguma ocorrência atípica, registrar na coluna final `Observacoes_Gerais_Sessao2`.
6. **Nomenclatura no Nexus:** `[ID]_hs01_assistido.c3d`, `[ID]_hs02_assistido.c3d`, `[ID]_hs03_assistido.c3d`.

> **Intervalo Inter-Blocos:** Repouso passivo total de **3 minutos sentado** com hidratação livre.

##### Bloco 2: Entradas Livres (3 Tentativas Obrigatórias | 90s Repouso)
1. **Execução:** Subida autônoma preferencial (*kick-up*) diretamente sobre a plataforma Bertec, sem nenhum auxílio externo. O participante realizará **obrigatoriamente as 3 tentativas** para viabilizar o cálculo da consistência/taxa de sucesso motor (ex: 3/3, 2/3 ou 1/3 acertos).
2. **Tentativas de Subida:** O atleta tem até **5 chutes de impulso** por tentativa para estabilizar no topo. Se não estabilizar em 5 tentativas, a tentativa é registrada como Falha.
3. **Estratégia de Poupança Neuromuscular:** O atleta pode buscar sua marca máxima de sustentação em uma tentativa. Nas demais, caso já tenha atingido sua marca representativa máxima, ele só precisa estabilizar e sustentar por **pelo menos 3,0 segundos contínuos** para validar o acerto técnico, descendo voluntariamente com controle sem necessidade de buscar a exaustão em todas as três, prevenindo a fadiga prévia para o HSW.
4. **Validação Técnica:**
   * **Tentativa Válida (OK):** Sustentação autônoma por **pelo menos 3,0 segundos contínuos**.
   * **Falha:** Queda antes de 3,0 segundos.
5. **Mapeamento do Pico:** É registrado em qual tentativa ocorreu o maior tempo de sustentação (`HS_Livre_Tentativa_Pico`: T1, T2 ou T3), permitindo investigar efeitos de calibração proprioceptiva vs. fadiga aguda.
6. **Nomenclatura no Nexus:** `[ID]_hs01_livre.c3d`, `[ID]_hs02_livre.c3d`, `[ID]_hs03_livre.c3d`.

---

#### 5.3 Handstand Walk (HSW) – Locomoção Dinâmica

> **Intervalo Pré-Teste Obrigatório:** Repouso passivo total de **10 minutos sentado**, garantindo dissipação completa de metabólitos, restauração dos estoques de fosfocreatina (PCr) e recuperação vestibular plena.

* **Dimensões da Pista Útil:** Corredor de **4,0 metros de comprimento linear útil** por **1,0 metro de largura**, demarcado com fitas discretas no solo.
* **Caixa de Partida (*Start Box*):** Retângulo de **60 cm de largura (X) por 35 cm de profundidade (Y)** demarcado com fita adesiva fosca no solo. A borda anterior da caixa coincide rigorosamente com o **Marco Zero ($Y = 0$)** do volume global.
* **Modos de Entrada Padronizados:**
  1. *De cima (Flying / Kick-up em passada):* Passo à frente, mãos dentro da caixa e subida contínua;
  2. *Mãos no solo (Base fixa):* Posição agachada/ajoelhada com as mãos já apoiadas dentro da caixa antes do chute;
  3. *Stop & Go:* Apoio das mãos, estabilização estática momentânea no alto e início da locomoção.
* **Regra Mandatória de Consistência Intra-Sujeito:** A modalidade de entrada definida na 1ª tentativa deve ser mantida estritamente em todas as tentativas válidas. Proibido alternar técnicas entre tentativas. Registrar o modo na coluna `HSW_Modo_Inicio` (`1 = De cima`, `2 = Mãos chão`, `3 = Stop&Go`).
* **Volume Otimizado de Tentativas:** **3 tentativas válidas** (em vez de 5, eliminando a degradação mecânica por fadiga periférica aguda nos ombros e punhos; intervalo de 90s entre tentativas).
* **Entradas por Tentativa:** O atleta tem direito a **até 3 entradas (subidas/chutes)** por tentativa caso ocorra erro no ajuste inicial da subida antes de iniciar os passos.
* **Critério de Validação da Marcha (Mínimo de 3 Passos):**
  * **Tentativa Válida:** Apoio das mãos na Start Box e percurso com **pelo menos 3 passos manuais alternados** antes de qualquer queda.
  * **Tentativa Nula (0 metros):** Quedas prematuras com apenas 1 ou 2 passos manuais não caracterizam locomoção cíclica contínua e são registradas como nulas/falha (0 metros).
* **Desfecho Primário do HSW:** **Mediana da Distância Percorrida (m)** entre as tentativas válidas, assegurando robustez frente a valores atípicos.
* **Nomenclatura no Nexus:** `[ID]_hsw01.c3d`, `[ID]_hsw02.c3d`, `[ID]_hsw03.c3d`.

---

### 6. DIRETRIZES NO VICON NEXUS: OPERADOR VS. PYTHON

Para não perder tempo durante a sessão experimental rotulando manualmente milhares de frames, a divisão de tarefas entre o software proprietário e o pipeline em Python foi rigorosamente otimizada:

| O que você FAZ no Vicon Nexus (Rápido) | O que o PYTHON faz Sozinho (Automatizado) |
| :--- | :--- |
| 1. No ensaio estático (`Cal.c3d`), executar **Reconstruct and Label** e garantir que pelo menos 1 frame tenha todos os marcadores rotulados (prioridade: cluster dorsal `C7`, `T10`, `LREF`, `RREF`, `RBAK` e os ombros `LSHO`/`RSHO`). | 1. **Gap Filling automático:** O Python interpola lacunas via splines PCHIP e remove saltos espúrios (>60 mm) sem intervenção manual. |
| 2. Nos ensaios dinâmicos (`hs` e `hsw`), disparar o **Auto-Labeling** e conferir rapidamente se o cluster dorsal, o `Apoio` (nas assistidas) e as extremidades estão com nomes atribuídos. | 2. **Reconstrução Rígida SVD:** Se os ombros (`LSHO`/`RSHO`) forem ocluídos pela cabeça/braços, o algoritmo de Kabsch recalcula a posição 3D exata a partir do cluster dorsal. |
| 3. Salvar o ensaio (**Save Trial**) e exportar os arquivos brutos `.c3d`. | 3. **Filtragem Digital:** Aplica filtro Butterworth passa-baixa 4ª ordem zero-lag (6 Hz cinemática e 20 Hz cinética). |
| | 4. **Detecção de Eventos:** Localiza algoritmicamente a soltura do avaliador (`dist_pesq > 250 mm`) e passadas no HSW. |

* **Modelo VSK Pré-Configurado:** Carregue previamente no Nexus o arquivo de modelo do sujeito (`.vsk`) contendo os marcadores adicionais (`LREF`, `RREF`, `RBAK` e `Apoio`). Assim, o Auto-Labeling rotula os marcadores extras automaticamente logo após a captura.

---

### 7. PIPELINE AUTOMATIZADO EM PYTHON: LIMPEZA, SVD E EXTRAÇÃO

Após o encerramento da coleta, o pós-processamento é executado em lote via terminal:

#### Passo 1: Transferir os Arquivos C3D Brutos
Mover todos os arquivos `.c3d` gerados no Nexus (`Cal.c3d`, `hs01 a hs03 assistido`, `hs01 a hs03 livre`, e `hsw01 a hsw05`) para a pasta:  
`coleta/PILOTO OFICIAL/02_SESSAO_LABIOCOM_CINEMATICA/dados_brutos_c3d/`

#### Passo 2: Executar o Pipeline Master
No terminal PowerShell, execute:
```powershell
cd "C:\Users\Gui\Documents\MESTRADO_HANDSTAND\coleta\PILOTO OFICIAL\02_SESSAO_LABIOCOM_CINEMATICA\pipeline_processamento"
python executar_pipeline_labiocom.py
```

#### Passo 3: Módulos Executados em Segundo Plano
1. **Reconstrução SVD & Limpeza (`pipeline_limpeza_automatica.py`):**
   * Lê `Cal.c3d`, calcula a geometria rígida do cluster dorsal (`C7`, `T10`, `LREF`, `RREF`) e recupera os ombros por SVD/Kabsch.
   * Elimina spikes (>60 mm), preenche lacunas via PCHIP e aplica filtro Butterworth (6 Hz cinemática, 20 Hz Bertec).
   * Salva os arquivos tratados em `dados_limpos_c3d/*_limpo.c3d`.
2. **Extração de Handstand Estático (`analisar_hs_oficial.py`):**
   * Detecta o início estável pelo afastamento do `Apoio` (>250 mm) nas assistidas ou elevação das pernas nas livres.
   * Extrai: **Tempo de Sustentação (s)**, **Distância CoP-CoM (mm)**, **Velocidade do CoP (mm/s)**, **Entropia Aproximada (ApEn AP e ML com $m=2$ e $r=0{,}2 \times \text{DP}$)**, **Verticalidade 3D (graus via Dot Product)**, **Extensão Cervical (graus)**, **Largura da Base de Apoio (mm)**, **Toe-out das Mãos (graus)**, **Altura do CoM (mm)** e **Comprimento de Membros (mm)**.
3. **Extração de Handstand Walk (`analisar_hsw_oficial.py`):**
   * Localiza toques e descolamentos manuais por cinemática dos punhos e dedos (`LFIN`/`RFIN`).
   * Extrai: **Distância Percorrida (m)**, **Duração da Marcha (s)**, **Velocidade Média (mm/s)**, **Cadência (passos/s)**, **Comprimento de Passada (mm)**, **Variabilidade Espaço-Temporal (CV %)**, **Fração de Duplo vs. Simples Suporte**, **Oscilação Médio-Lateral do CoM (mm)**, **Verticalidade Dinâmica (graus)** e **Extensão Cervical (graus)**.

#### Passo 4: Matriz de Saída
Os resultados consolidados tentativa por tentativa são salvos em:  
`coleta/PILOTO OFICIAL/02_SESSAO_LABIOCOM_CINEMATICA/resultados/variaveis_labiocom_por_tentativa.csv`

---

### 8. CONSOLIDAÇÃO FINAL DO DATASET (SPSS READY)

Ao final de ambas as sessões (LaCiDH e LaBioCoM), o script consolidador integra todos os dados dos participantes (Questionário Online + Força e Composição LaCiDH + Cinemática e Cinética LaBioCoM):

```powershell
cd "C:\Users\Gui\Documents\MESTRADO_HANDSTAND\coleta\PILOTO OFICIAL\03_CONSOLIDACAO_DATASET\scripts"
python consolidar_dataset_mestrado.py
```

* **Arquivo Gerado:** `coleta/PILOTO OFICIAL/03_CONSOLIDACAO_DATASET/dataset_final/dataset_mestrado_completo_SPSS.csv`.
* **Pronto para Estatística:** Planilha parametrizada com variáveis numéricas agregadas (melhor tempo de sustentação no HS assistido, taxas de sucesso no HS livre e medianas no HSW dinâmico) pronta para importação direta no SPSS para alimentação dos **Modelos 1 a 6 de Regressão**.

---

### 9. REFERÊNCIAS BIBLIOGRÁFICAS

* **BORG, F. G.; LAXÅBACK, G.** Entropy of balance—some recent results. *Journal of NeuroEngineering and Rehabilitation*, v. 7, n. 1, p. 38, 2010.
* **CAVANAUGH, J. T. et al.** Detecting altered postural control after cerebral concussion in athletes with normal postural stability. *British Journal of Sports Medicine*, v. 39, n. 11, p. 805-811, 2005.
* **CHALLIS, J. H.** A procedure for determining rigid body transformation parameters. *Journal of Biomechanics*, v. 28, n. 6, p. 733-737, 1995.
* **DAVIS, R. B. et al.** A clinical gait analysis method. *Human Movement Science*, v. 10, n. 5, p. 575-587, 1991.
* **DONKER, S. F. et al.** Regularity of center-of-pressure trajectories reflects the degree of attention invested in postural control. *Experimental Brain Research*, v. 181, n. 1, p. 1-11, 2007.
* **FELLIN, R. E. et al.** Comparison of methods for kinematic identification of footstrike and toe-off during overground and treadmill running. *Journal of Science and Medicine in Sport*, v. 13, n. 6, p. 646-650, 2010.
* **KABSCH, W.** A solution for the best rotation to relate two sets of vectors. *Acta Crystallographica Section A*, v. 32, n. 5, p. 922-923, 1976.
* **KERWIN, D. G.; TREWARTHA, G.** Strategies for maintaining a handstand in the anterior-posterior direction. *Medicine and Science in Sports and Exercise*, v. 33, n. 7, p. 1182-1188, 2001.
* **PINCUS, S. M.** Approximate entropy as a measure of system complexity. *Proceedings of the National Academy of Sciences*, v. 88, n. 6, p. 2297-2301, 1991.
* **PRYHODA, M. et al.** Task Specific and General Patterns of Joint Motion Variability in Upright- and Hand-Standing Postures. *Entropy*, v. 24, n. 7, p. 909, 2022.
* **RAMDANI, S. et al.** On the use of sample entropy to analyze human postural sway data. *Medical Engineering & Physics*, v. 31, n. 8, p. 1023-1031, 2009.
* **ROERDINK, M. et al.** Dynamical structure of center-of-pressure trajectories in patients recovering from stroke. *Experimental Brain Research*, v. 174, n. 2, p. 256-266, 2006.
* **STERGIOU, N.** *Nonlinear Analysis for Human Movement Variability*. Boca Raton: CRC Press / Taylor & Francis, 2016.
* **WINTER, D. A.** *Biomechanics and Motor Control of Human Movement*. 4th ed. Hoboken: John Wiley & Sons, 2009.
* **WYATT, H. E. et al.** Bidirectional causal control in the dynamics of handstand balance. *Scientific Reports*, v. 11, n. 1, p. 405, 2021.
* **YENTES, J. M. et al.** The appropriate use of approximate entropy and sample entropy with short data sets in human locomotion. *Annals of Biomedical Engineering*, v. 41, n. 2, p. 349-365, 2013.
* **ZENI, J. A. et al.** Two simple methods for determining gait events during treadmill and overground walking using kinematic data. *Gait & Posture*, v. 27, n. 4, p. 710-714, 2008.
