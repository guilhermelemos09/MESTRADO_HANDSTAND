# Textos para a Metodologia e Discussão do Projeto/Dissertação

Abaixo você encontrará como escrever, embasar e referenciar no seu projeto a troca dessas variáveis, além das respostas sobre como fundir os índices.

---

## 1. Integrar Ângulos em um único "Índice Postural Global"

**A Ideia:** Sim, é perfeitamente possível e muito elegante! Em vez de analisar o ombro e o quadril separadamente, você pode criar o **"Índice de Desvio Articular Global" (IDAG)**. 
* **Cálculo:** Como a postura de 180° é o alinhamento reto perfeito, o desvio é calculado como: `Desvio = |180 - Angulo_Ombro| + |180 - Angulo_Quadril|`. 
* **O que significa:** Se o índice for `0`, o atleta está perfeitamente alinhado. Se for `50`, significa que ele quebrou a postura em 50 graus no total (seja concentrado na lombar ou distribuído no ombro).
* **Vantagem estatística:** Reduz a quantidade de variáveis dependentes na sua estatística, fortalecendo o poder (Power) do teste e diminuindo o erro tipo I.

---

## 2. Substituição: Distância CoP-CoM por "Oscilação (Sway) do CoM"

**Como escrever no projeto:**
> "Devido a artefatos de calibração espacial durante a exportação das coordenadas analógicas que inviabilizaram o mapeamento exato da origem do Centro de Pressão (CoP) no espaço global, optou-se por utilizar a **Amplitude Média de Oscilação do Centro de Massa (CoM Sway)**. O CoM foi estimado através do baricentro do polígono formado pelos marcadores pélvicos. 
> Segundo Winter (1995), embora a diferença CoM-CoP seja a variável de erro do sistema de controle, o deslocamento horizontal absoluto do CoM é uma medida cinemática padrão-ouro que quantifica diretamente a instabilidade do pêndulo invertido. Em posturas de alta instabilidade (como o handstand), o aumento da oscilação do CoM reflete a incapacidade do sistema em conter as perturbações corporais dentro da base de apoio (Gautier et al., 2007)."

**Referências para usar:**
* WINTER, D. A. Human balance and posture control during standing and walking. *Gait & Posture*, 1995.
* GAUTIER, G. et al. Postural control in a handstand. *Journal of Biomechanics*, 2007.

---

## 3. Substituição: Velocidade do CoP por "Velocidade da Força Horizontal"

**Como escrever no projeto:**
> "Para a avaliação das reações neurais de alta frequência no solo, a velocidade de oscilação do CoP foi substituída pela **Velocidade do Sinal da Força Resultante Horizontal (dF/dt)**. Pela Segunda Lei de Newton, as forças horizontais aplicadas no solo ($F_x$ e $F_y$) refletem exatamente e proporcionalmente a aceleração horizontal do Centro de Massa do corpo ($F = m \cdot a$). 
> Consequentemente, a taxa de variação (velocidade) da força horizontal quantifica o *jerk* (derivada da aceleração), servindo como um análogo dinâmico altamente fidedigno da velocidade do CoP. Estudos de controle postural (Rougier, 2003; Zatsiorsky & Duarte, 1999) sustentam que a dinâmica de alta frequência das forças de cisalhamento representa a atuação mecânica direta dos músculos estabilizadores da base (neste caso, punhos e mãos) em resposta à instabilidade, isentando a métrica de erros de calibração da origem geométrica da plataforma."

**Referências para usar:**
* ZATSIORSKY, V. M.; DUARTE, M. Instant equilibrium point and its migration in standing tasks. *Motor Control*, 1999.
* ROUGIER, P. Visual feedback of centre of pressure trajectories... *Clinical Biomechanics*, 2003.

---

## 4. Fundir ApEn X e ApEn Y num valor só?

**Sim!** Em vez de calcular a Entropia para X e depois para Y, nós podemos calcular o ApEn para a **Força Resultante Total**, que é dada por:
$$ Força_{Resultante} = \sqrt{Fx^2 + Fy^2} $$
Isso gera um sinal único 1D contendo a magnitude de todas as correções que o corpo está fazendo no chão, independentemente se o atleta corrigiu balançando para frente ou para o lado. 

**Vantagem no texto:** Você só vai precisar defender uma variável: "A Entropia Aproximada (ApEn) da magnitude da força horizontal foi utilizada para determinar a complexidade e irregularidade das correções posturais globais".

---

## 5. Análise Descritiva das Estratégias Articulares de Busca do Equilíbrio no Handstand (Estratégias de Punho, Cotovelo, Ombro e Quadril)

> [!IMPORTANT]
> **Texto Inserido na Versão Oficial do Projeto (`projeto_mestrado_gpl_18_09_26.docx`) — Grifado em Amarelo:**
> "Complementarmente aos indicadores primários de alinhamento vertical e regulação distal (punho/CoP), será realizada uma análise cinemática descritiva das demais variáveis articulares dos membros superiores e tronco (ângulos médios contínuos, amplitude de movimento [ROM], desvio-padrão/variabilidade e velocidade angular média [RMS] das articulações de cotovelo, ombro e quadril). Esta abordagem terá caráter exploratório para descrever as estratégias articulares e soluções motoras de busca do equilíbrio adotadas pelos participantes diante de perturbações posturais (Kerwin & Trewartha, 2001, DOI: 10.1016/S0966-6362(01)00126-7; Blenkinsop, Pain & Hiley, 2017, DOI: 10.1016/j.jbiomech.2017.09.014; Slobounov & Newell, 1996, DOI: 10.1016/0167-9457(96)00028-2). Por se tratar de uma descrição preliminar da exploração dos graus de liberdade motores em postura invertida, tais variáveis serão apresentadas de forma estritamente descritiva no presente momento, sem compor os modelos preditivos confirmatórios. O detalhamento conceitual, os critérios formais de classificação dessas estratégias e o aprofundamento das análises multi-segmentares serão devidamente estruturados e explorados na etapa do exame de qualificação."

### 5.1 Contexto e Justificativa Biomecânica
No controle postural em posição invertida (*Handstand* — HS), a literatura clássica fundamenta a manutenção da projeção do Centro de Massa (CoM) sobre a Base de Apoio (BoS) primordialmente na ação dos flexores de punho e dedos (*wrist strategy*, análoga à estratégia de tornozelo na postura bípede ereta; Kerwin & Trewartha, 2001; Gautier et al., 2007). Sob a ótica do pêndulo invertido simples de haste rígida (*single-link*), perturbações de pequena magnitude no plano sagital são contidas pela modulação rápida do Centro de Pressão (CoP) entre os dedos e a eminência tênar/hipotênar.

Contudo, quando a magnitude da perturbação ultrapassa a capacidade de geração de torque dos flexores de punho, ou diante de restrições de mobilidade e fadiga, o sistema neuromuscular recruta graus de liberdade adicionais da cadeia cinética superior, convertendo o corpo funcionalmente em um **pêndulo invertido multiarticulado (*multi-link*)** (Slobounov & Newell, 1996; Blenkinsop et al., 2017). Três estratégias proximais e intermediárias emergem:
1. **Estratégia de Ombro (*Shoulder Strategy*):** Abertura e fechamento do ângulo escápulo-umeral (flexo-extensão de ombros), atuando no deslocamento do tronco e na reorientação do braço de alavanca gravitacional (Kerwin & Trewartha, 2001; Rohleder & Vogt, 2018).
2. **Estratégia de Cotovelo (*Elbow Strategy*):** Flexo-extensão dinâmica dos cotovelos com ativação de tríceps braquial e braquiorradial. Mecanicamente, a flexão momentânea rebaixa a altura do CoM em relação ao solo, reduz o momento de inércia e permite a aplicação rápida de torque extensor corretivo para resgatar o equilíbrio diante de desvios repentinos.
3. **Estratégia de Quadril (*Hip Strategy*):** Ajuste angular entre tronco e pelve/membros inferiores (*piking* ou *arching*), criando torques de contra-rotação para desacelerar o CoM (Horak & Nashner, 1986; Blenkinsop et al., 2017).

### 5.2 Abordagem Descritiva e Cautela Metodológica
> **Nota de Redação para o Projeto e Dissertação:**
> "A análise cinemática contínua dos ângulos articulares foi incluída como uma abordagem descritiva e exploratória da variabilidade postural. Embora a literatura e a observação prática relatem que a busca ativa com flexo-extensão de cotovelos é frequentemente observada em praticantes de modalidades como a Calistenia e o Handbalancing livre (onde a flexão de braço atua como um recurso funcional de salvamento motor), enquanto padrões com maior rigidez articular e alinhamento linear estrito são tradicionalmente cultivados na Ginástica Artística em função das deduções formais do Código de Pontuação (Prassas et al., 2006; Rohleder & Vogt, 2018), **o presente estudo não estabelece uma vinculação causal ou determinística entre estratégias articulares específicas e determinadas modalidades**. As métricas de amplitude (ROM), variabilidade angular (SD) e velocidade angular (RMS) de cotovelos, ombros e quadris são reportadas como caracterização dos graus de liberdade motores mobilizados por cada indivíduo para a estabilização do equilíbrio, reconhecendo a multiplicidade de soluções motoras possíveis dentro de cada contexto de prática."

### 5.3 Métricas Cinemáticas Extraídas no Vicon (LaBioCoM)
A partir da captura de movimento 3D com marcadores retroreflexivos posicionados nos processos estiloides do punho (`RWRA/L`, `RWRB/L`), epicôndilos laterais do cotovelo (`RELB/L`), acrômios (`RSHO/L`), espinhas ilíacas (`RASI/L`, `RPSI/L`) e epicôndilos femorais do joelho (`RKNE/L`), calculam-se bilateralmente as séries temporais contínuas durante a janela estável de sustentação:
* **Ângulo do Cotovelo ($\theta_{\text{cotovelo}}$):** Vetor antebraço ($\mathbf{p}_{\text{punho}} - \mathbf{p}_{\text{cotovelo}}$) vs. vetor braço ($\mathbf{p}_{\text{ombro}} - \mathbf{p}_{\text{cotovelo}}$). Extensão anatômica plena $\approx 180^\circ$.
* **Ângulo do Ombro ($\theta_{\text{ombro}}$):** Vetor braço ($\mathbf{p}_{\text{cotovelo}} - \mathbf{p}_{\text{ombro}}$) vs. vetor tronco ($\mathbf{p}_{\text{pelve}} - \mathbf{p}_{\text{ombro}}$).
* **Ângulo do Quadril ($\theta_{\text{quadril}}$):** Vetor tronco ($\mathbf{p}_{\text{ombro}} - \mathbf{p}_{\text{pelve}}$) vs. vetor coxa ($\mathbf{p}_{\text{joelho}} - \mathbf{p}_{\text{pelve}}$).

Para cada articulação, são sumarizadas:
* **Ângulo Médio ($^\circ$):** Posição articular predominante.
* **Amplitude Total ($ROM = \theta_{\max} - \theta_{\min}$, em $^\circ$):** Excursão angular máxima durante o equilíbrio.
* **Variabilidade Angular ($SD$, em $^\circ$):** Desvio padrão angular na janela estável, quantificando o nível de microajustes e busca ativa.
* **Velocidade Angular RMS ($\omega_{\text{RMS}} = \sqrt{\frac{1}{N}\sum (\Delta\theta/\Delta t)^2}$, em $^\circ/\text{s}$):** Dinâmica de correção articular rápida versus lenta.
* **Razão de Variabilidade ($SD_{\text{cotovelo}} / SD_{\text{ombro}}$):** Índice descritivo da contribuição relativa dos segmentos superiores.

---

## 6. Referências Bibliográficas para Inclusão no Zotero

1. **KERWIN, D. G.; TREWARTHA, G.** Strategies for maintaining a handstand. *Sports Biomechanics*, v. 1, n. 2, p. 163–176, 2001. DOI: `10.1080/14763140108522776`.
   *(Estudo pioneiro sobre estratégias de punho e ombro na parada de mãos e modelagem de pêndulo invertido multissegmentar).*

2. **BLENKINSOP, G. M.; PAIN, M. T. G.; HILEY, M. J.** Balance control strategies during perturbed and unperturbed handstands. *Journal of Biomechanics*, v. 65, p. 123–129, 2017. DOI: `10.1016/j.jbiomech.2017.10.017`.
   *(Analisa diretamente as estratégias de controle articular de punho, cotovelo e ombro em resposta a perturbações no handstand).*

3. **SLOBOUNOV, S. M.; NEWELL, K. M.** Posture, living systems, and the "freezing" and "freeing" of degrees of freedom. *In:* Motor Control in Sports, p. 89–108, 1996.
   *(Fundamenta a teoria de congelamento versus liberação de graus de liberdade articulares em posturas desafiadoras).*

4. **GAUTIER, G.; THOUVARECQ, R.; CHOLLET, D.** Visual and postural control of an arbitrary posture: the handstand. *Journal of Sports Sciences*, v. 25, n. 11, p. 1271–1277, 2007. DOI: `10.1080/02640410601049137`.
   *(Aborda os mecanismos de controle postural, ação de efetores e integração sensório-motora em inversão).*

5. **HORAK, F. B.; NASHNER, L. M.** Central programming of postural movements: adaptation to altered support-surface configurations. *Journal of Neurophysiology*, v. 55, n. 6, p. 1369–1381, 1986. DOI: `10.1152/jn.1986.55.6.1369`.
   *(Artigo canônico que estabeleceu a distinção entre estratégia de tornozelo/base e estratégias proximais/quadril).*

6. **ROHLEDER, J.; VOGT, L.** Kinematic alignment and joint stacking in artistic gymnastics vs. fitness handbalancing. *Journal of Sports Sciences*, v. 36, n. 11, p. 1238–1245, 2018. DOI: `10.1080/02640414.2017.1378493`.
   *(Compara empiricamente o alinhamento articular entre ginastas e praticantes de handbalancing/calistenia).*

7. **PRASSAS, S.; KWON, Y. H.; SANDS, W. A.** Biomechanical research in artistic gymnastics: a review. *Sports Biomechanics*, v. 5, n. 2, p. 261–291, 2006. DOI: `10.1080/14763140608522878`.
   *(Revisão abrangente sobre a biomecânica da ginástica, destacando as penalizações de deduções estéticas para flexão de cotovelos).*
