// App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import tarotDeck from './tarotDeck';



function App() {
  const [selectedCard, setSelectedCard] = useState(null);
  const [reading, setReading] = useState("");
  const [readingHistory, setReadingHistory] = useState([]);
  const [readingType, setReadingType] = useState('Amor e Relacionamentos');
  const [layoutType, setLayoutType] = useState('Leitura Três Cartas');
  const [isLoading, setIsLoading] = useState(false);


  // Defina as variáveis para os detalhes da carta.
  const [showCardDetails, setShowCardDetails] = useState(false);
  const [cardDetails, setCardDetails] = useState({ name: '', description: '', meaning: '' });

  // Função para selecionar uma carta
  const selectCard = (cardKey) => {
    setSelectedCard(cardKey);
    // Aqui você pode definir as informações detalhadas da carta com base na carta selecionada.
    setCardDetails(tarotDeck[cardKey]);
    setShowCardDetails(true); // Mostra os detalhes da carta.
  };

  // Função para renderizar os detalhes da carta
  const renderCardDetails = () => {
    if (!showCardDetails) return null;

    return (
      <div className="card-details">
        <h3>{cardDetails.name}</h3>
        <p>{cardDetails.description}</p>
        <p>{cardDetails.meaning}</p>
        {/* Adicione um botão para ocultar os detalhes da carta. */}
        <button onClick={() => setShowCardDetails(false)}>Fechar Detalhes</button>
      </div>
    );
  };


  const getTarotReading = async () => {
    if (!selectedCard) {
      alert("Por favor, selecione uma carta primeiro.");
      return;
    }
    setIsLoading(true);
    const cardDescription = tarotDeck[selectedCard].description;
    const prompt = `Realize uma leitura de Tarô no tema '${readingType}' utilizando o layout '${layoutType}' para a carta com a seguinte descrição: '${cardDescription}'. Por favor, forneça orientações e insights sobre o assunto que possam ser úteis e esclarecedores para o cliente.`;

    try {
      const response = await axios.post('https://api.openai.com/v1/chat/completions', {
        model: "gpt-3.5-turbo",
        messages: [{
          role: "system",
          content: "Bem-vindo à Plataforma de Tarô! Estás a conversar com um leitor de tarô. Sinta-te à vontade para fazer a tua pergunta ou escolher uma leitura específica. Estou aqui para ajudar."
        }, {
          role: "user",
          content: prompt
        }]
      }, {
        headers: {
          'Authorization': `Bearer ${process.env.REACT_APP_CHATGPT_API_KEY}`
        }
      });

      const receivedReading = response.data.choices[0].message.content;
      setReading(receivedReading);
      setReadingHistory(prevHistory => [...prevHistory, receivedReading]);
      setIsLoading(false);
    } catch (error) {
      console.error("Erro ao obter a leitura de tarô:", error);
      alert("Erro ao obter a leitura.");
      setIsLoading(false);
    }
  };


  return (
    <div className="App">
      <header className="App-header">
        <p>Bem-vindo à Plataforma de Tarô</p>
        <div className="tarot-cards" >
          {Object.keys(tarotDeck).map((cardKey, index) => (
            <img
              key={index}
              src={`/images/${cardKey}`}
              alt={tarotDeck[cardKey].name}
              className={`card ${selectedCard === cardKey ? 'card-selected' : ''} card-enter-animation`}
              onClick={() => selectCard(cardKey)}
            />
          ))}
          {isLoading && <p>Carregando...</p>}
  
          {!isLoading && reading && <p className="reading">{reading}</p>}
        </div>
        <select value={readingType} onChange={e => setReadingType(e.target.value)}>
          <option value="Amor e Relacionamentos">Amor e Relacionamentos</option>
          <option value="Carreira e Finanças">Carreira e Finanças</option>
          <option value="Saúde e Bem-Estar">Saúde e Bem-Estar</option>
          <option value="Espiritual">Espiritual</option>
          <option value="Decisões e Escolhas">Decisões e Escolhas</option>
          <option value="Família e Amigos">Família e Amigos</option>
        </select>

        <select value={layoutType} onChange={e => setLayoutType(e.target.value)}>
          <option value="Leitura Três Cartas">Leitura Três Cartas</option>
          <option value="Leitura Cruz Celta">Leitura Cruz Celta</option>
          <option value="Leitura Uma Carta">Leitura Uma Carta</option>
          <option value="Leitura Sim/Não">Leitura Sim/Não</option>
        </select>
        <button onClick={getTarotReading}>Obter Leitura de Tarô</button>

        {renderCardDetails()} { }

        <div className="reading-history">
          <h3>Histórico de Leituras</h3>
          <ul>
            {readingHistory.map((reading, index) => (
              <li key={index}>{reading}</li>
            ))}
          </ul>
        </div>
      </header>
    </div>
  );
}

export default App;
