# ♻️ Totem de Reciclagem Sustentável com Leitor Facial

Projeto de Extensão (PEI) focado em gamificar a coleta seletiva através de reconhecimento biometral. O sistema identifica o usuário na hora do descarte e atribui pontos de reciclagem automaticamente.

✨ **Diferencial:** Este projeto foi projetado para rodar 100% na nuvem. **Você não precisa instalar Python, bibliotecas ou clonar nada no seu computador local para testar!**

## 🚀 Tecnologias Utilizadas
* **Backend:** Python e Flask (Monolito)
* **Inteligência Artificial:** `dlib` e `face_recognition` (Mapeamento de 68 pontos faciais)
* **Processamento de Imagem:** Pillow (PIL) para sanitização de perfis de cor e remoção de transparências Alpha.
* **Banco de Dados:** SQLite3 (Nativo)
* **Frontend:** HTML5, CSS3, Vanilla JS (Com ajuste dinâmico de canvas para acesso nativo a câmeras mobile sem distorção).

## ☁️ Como testar agora mesmo (Zero Instalação)

Utilizando o GitHub Codespaces, você sobe o servidor Linux e a Inteligência Artificial diretamente pelo seu navegador:

1. No topo desta página do repositório, clique no botão verde **`<> Code`**.
2. Mude para a aba **`Codespaces`** e clique em **`Create codespace on main`**.
3. O GitHub abrirá um ambiente VS Code completo no seu navegador. Aguarde alguns segundos até o terminal carregar na parte inferior.
4. No terminal, crie a "bolha" de isolamento e instale as dependências (o servidor Linux fará a compilação do motor de IA automaticamente):
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt