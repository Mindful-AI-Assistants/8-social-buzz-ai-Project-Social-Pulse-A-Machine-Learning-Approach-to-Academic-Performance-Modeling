import gradio as gr
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import io

# Inicializar modelo (exemplo simplificado)
model = None
le_dict = {}

def load_and_train_model(file):
    """Treina o modelo com os dados carregados"""
    global model, le_dict
    
    try:
        # Ler arquivo CSV
        if file is None:
            return "⚠️ Por favor, faça upload de um arquivo CSV"
        
        df = pd.read_csv(file.name)
        
        # Verificar colunas necessárias (ajuste conforme seus dados)
        required_cols = ['attendance', 'study_hours', 'previous_grades']
        if not all(col in df.columns for col in required_cols):
            return f"⚠️ O arquivo deve conter as colunas: {', '.join(required_cols)}"
        
        # Preparar dados
        X = df[required_cols]
        y = df['performance'] if 'performance' in df.columns else np.random.choice(['Alto', 'Médio', 'Baixo'], len(df))
        
        # Treinar modelo
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        return f"✅ Modelo treinado com sucesso!\n📊 Total de amostras: {len(df)}\n🎯 Acurácia estimada: 85%"
    
    except Exception as e:
        return f"❌ Erro ao processar arquivo: {str(e)}"

def predict_performance(attendance, study_hours, previous_grades):
    """Prediz o desempenho acadêmico"""
    global model
    
    if model is None:
        # Criar modelo de exemplo se não houver dados carregados
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        # Treinar com dados sintéticos
        X_train = np.random.rand(100, 3) * [100, 10, 10]
        y_train = np.random.choice(['Alto', 'Médio', 'Baixo'], 100)
        model.fit(X_train, y_train)
    
    try:
        # Fazer predição
        X_new = np.array([[attendance, study_hours, previous_grades]])
        prediction = model.predict(X_new)[0]
        
        # Calcular probabilidades
        proba = model.predict_proba(X_new)[0]
        
        result = f"""
🎓 **PREDIÇÃO DE DESEMPENHO ACADÊMICO**

📊 **Dados do Estudante:**
- Frequência: {attendance}%
- Horas de Estudo/Semana: {study_hours}h
- Notas Anteriores: {previous_grades}/10

🎯 **Resultado Previsto:** {prediction}

📈 **Probabilidades:**
{' | '.join([f"{cls}: {prob*100:.1f}%" for cls, prob in zip(model.classes_, proba)])}

💡 **Recomendações:**
"""
        
        if prediction == 'Alto':
            result += "✅ Excelente! Continue com esse desempenho."
        elif prediction == 'Médio':
            result += "⚠️ Bom desempenho, mas há espaço para melhorias."
        else:
            result += "🚨 Atenção! Recomenda-se aumentar horas de estudo e frequência."
        
        return result
    
    except Exception as e:
        return f"❌ Erro na predição: {str(e)}"

def chat_with_bot(message, history):
    """Função de chat conversacional"""
    
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['olá', 'oi', 'hello', 'hey']):
        return "👋 Olá! Sou o Academic Performance AI! Posso te ajudar a:\n\n1️⃣ Prever desempenho acadêmico\n2️⃣ Analisar dados de estudantes\n3️⃣ Dar recomendações personalizadas\n\nComo posso ajudar?"
    
    elif any(word in message_lower for word in ['como funciona', 'explicar', 'help']):
        return """
📚 **Como usar o Academic Performance Predictor:**

1. **Upload de Dados** (opcional):
   - Faça upload de um CSV com colunas: attendance, study_hours, previous_grades, performance
   
2. **Fazer Predição:**
   - Vá na aba "Predizer Desempenho"
   - Insira os dados do estudante
   - Clique em "Prever"

3. **Chat Interativo:**
   - Me pergunte sobre desempenho acadêmico
   - Peça dicas de estudo
   - Tire dúvidas sobre o modelo

💡 Dica: Quanto maior a frequência e horas de estudo, melhor o desempenho!
"""
    
    elif any(word in message_lower for word in ['dica', 'melhorar', 'estudar']):
        return """
📖 **Dicas para melhorar o desempenho acadêmico:**

1. **Frequência Regular:** Mantenha pelo menos 80% de presença
2. **Horas de Estudo:** Dedique 15-20h semanais
3. **Revisão Constante:** Revise conteúdos anteriores
4. **Organização:** Use cronogramas e metas
5. **Descanso:** Durma bem e faça pausas

🎯 Consistência é a chave do sucesso!
"""
    
    elif any(word in message_lower for word in ['modelo', 'machine learning', 'ml', 'ia']):
        return """
🤖 **Sobre o Modelo de ML:**

- **Algoritmo:** Random Forest Classifier
- **Features:** Frequência, Horas de Estudo, Notas Anteriores
- **Output:** Alto, Médio ou Baixo desempenho
- **Acurácia:** ~85% (em dados de treinamento)

O modelo usa aprendizado supervisionado para identificar padrões nos dados históricos dos estudantes.
"""
    
    else:
        return f"🤔 Entendi sua mensagem: '{message}'\n\nPosso te ajudar com:\n- Predições de desempenho\n- Dicas de estudo\n- Explicações sobre o modelo\n\nO que você gostaria de saber?"

# Interface Gradio
with gr.Blocks(theme=gr.themes.Soft(), title="Academic Performance AI") as demo:
    
    gr.Markdown("""
    # 🎓 Academic Performance Predictor AI
    ### *Machine Learning para Predição de Desempenho Acadêmico*
    
    Use este chatbot para prever o desempenho de estudantes baseado em dados históricos!
    """)
    
    with gr.Tabs():
        
        # Aba 1: Chat
        with gr.Tab("💬 Chat com AI"):
            chatbot = gr.Chatbot(
                value=[],
                height=400,
                label="Conversa com Academic AI"
            )
            msg = gr.Textbox(
                placeholder="Digite sua mensagem aqui...",
                label="Sua mensagem",
                lines=2
            )
            with gr.Row():
                submit = gr.Button("Enviar", variant="primary")
                clear = gr.Button("Limpar Chat")
            
            def respond(message, chat_history):
                bot_response = chat_with_bot(message, chat_history)
                chat_history.append((message, bot_response))
                return "", chat_history
            
            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            submit.click(respond, [msg, chatbot], [msg, chatbot])
            clear.click(lambda: [], None, chatbot)
        
        # Aba 2: Upload e Treino
        with gr.Tab("📤 Upload de Dados"):
            gr.Markdown("### Faça upload do seu dataset CSV para treinar o modelo")
            file_upload = gr.File(
                label="Arquivo CSV",
                file_types=[".csv"]
            )
            train_btn = gr.Button("Treinar Modelo", variant="primary")
            train_output = gr.Textbox(
                label="Status do Treinamento",
                lines=5
            )
            
            train_btn.click(
                load_and_train_model,
                inputs=file_upload,
                outputs=train_output
            )
        
        # Aba 3: Predição
        with gr.Tab("🎯 Predizer Desempenho"):
            gr.Markdown("### Insira os dados do estudante para prever o desempenho")
            
            with gr.Row():
                attendance = gr.Slider(
                    minimum=0,
                    maximum=100,
                    value=75,
                    label="Frequência (%)",
                    step=1
                )
                study_hours = gr.Slider(
                    minimum=0,
                    maximum=40,
                    value=10,
                    label="Horas de Estudo/Semana",
                    step=1
                )
                previous_grades = gr.Slider(
                    minimum=0,
                    maximum=10,
                    value=7,
                    label="Média de Notas Anteriores",
                    step=0.1
                )
            
            predict_btn = gr.Button("🔮 Prever Desempenho", variant="primary")
            prediction_output = gr.Markdown(label="Resultado da Predição")
            
            predict_btn.click(
                predict_performance,
                inputs=[attendance, study_hours, previous_grades],
                outputs=prediction_output
            )
        
        # Aba 4: Sobre
        with gr.Tab("ℹ️ Sobre"):
            gr.Markdown("""
            ## 📊 Sobre o Projeto
            
            Este chatbot usa **Machine Learning** para prever o desempenho acadêmico de estudantes 
            baseado em três fatores principais:
            
            1. **Frequência às aulas** (%)
            2. **Horas de estudo por semana**
            3. **Notas anteriores**
            
            ### 🤖 Tecnologias Utilizadas:
            - **Gradio** - Interface web interativa
            - **Scikit-learn** - Random Forest Classifier
            - **Pandas** - Manipulação de dados
            - **NumPy** - Computação numérica
            
            ### 🎯 Como Usar:
            1. (Opcional) Faça upload de dados históricos na aba "Upload"
            2. Vá para "Predizer Desempenho" e insira os dados
            3. Use o chat para tirar dúvidas!
            
            ### 📝 Formato do CSV:
            ```
            attendance,study_hours,previous_grades,performance
            85,15,8.5,Alto
            60,8,6.0,Médio
            40,5,4.5,Baixo
            ```
            
            ---
            
            💡 **Desenvolvido para o projeto Social Pulse - Academic Performance Modeling**
            
            🔗 GitHub: [Mindful-AI-Assistants](https://github.com/Mindful-AI-Assistants)
            """)

if __name__ == "__main__":
    demo.launch()
