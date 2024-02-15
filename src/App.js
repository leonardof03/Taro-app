import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import tarotDeck from './tarotDeck';

function App() {
  const [readingType, setReadingType] = useState('Amor e Relacionamentos');
  const [layoutType, setLayoutType] = useState('Leitura Três Cartas');
  const [isLoading, setIsLoading] = useState(false);
  const [userQuestion, setUserQuestion] = useState("");
  const [selectedCard, setSelectedCard] = useState(null);
  const [reading, setReading] = useState("");
  const [readingHistory, setReadingHistory] = useState([]);

  const selectRandomCard = () => {
    const cardKeys = Object.keys(tarotDeck);
    const randomIndex = Math.floor(Math.random() * cardKeys.length);
    const randomCardKey = cardKeys[randomIndex];
    return randomCardKey;
  };

  const getTarotReading = async () => {
    if (!userQuestion) {
      alert("Por favor, digite sua pergunta personalizada.");
      return;
    }

    setIsLoading(true);

    try {
      const selectedCardKey = selectRandomCard();
      setSelectedCard(selectedCardKey);

      const response = await axios.post('https://api.openai.com/v1/chat/completions', {
        model: "gpt-3.5-turbo",
        messages: [{
          role: "system",
          content: "Bem-vindo à Plataforma de Tarô! Estás a conversar com um leitor de tarô. Sinta-te à vontade para fazer a tua pergunta ou escolher uma leitura específica. Estou aqui para ajudar."
        }, {
          role: "user",
          content: `Realiza uma leitura de Tarô no tema '${readingType}' utilizando o layout '${layoutType}' para a carta "${tarotDeck[selectedCardKey]?.name}" com a seguinte descrição: '${tarotDeck[selectedCardKey]?.description}'. Por favor, forneça orientações e insights sobre o assunto que possam ser úteis e esclarecedores para o cliente. Pergunta do usuário: '${userQuestion}'`
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

  const resetApp = () => {
    setSelectedCard(null);
    setReading("");
    setUserQuestion("");
    setIsLoading(false);
    setReadingType('Amor e Relacionamentos');
    setLayoutType('Leitura Três Cartas');
  };
  return (
    <div className="tarot-container">
      <header className="App-header">
        <div className="top-bar">
          <p>Bem-vindo à Plataforma de Tarô do Leonardinho</p>
          <div className="input-container">
            <textarea
              value={userQuestion}
              onChange={(e) => setUserQuestion(e.target.value)}
              placeholder="Digite sua pergunta personalizada"
            />
            <div className="button-group">
              <button onClick={getTarotReading}>Obter Leitura de Tarô</button>
              <button onClick={resetApp}>Clear</button>
            </div>
          </div>
          <div className="select-container">
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
          </div>
        </div>
  
        <div className="tarot-cards">
          {isLoading ? (
            <div className="tarot-loading-animation">
              <img src="/images/tarot.gif" alt="Baralho de cartas de tarô girando" />
            </div>
            
          ) : (
            <div className="card-container"> {/* Novo contêiner para a carta de tarô */}
              <img
                src={`/images/${selectedCard}`}
                alt={tarotDeck[selectedCard]?.name}
                className={`card card-selected`}
              />
            </div>
          )}
          {!isLoading && selectedCard && (
            <div className="card-details">
              <h3>{tarotDeck[selectedCard]?.name}</h3>
              <p>{tarotDeck[selectedCard]?.description}</p>
              <p>{tarotDeck[selectedCard]?.meaning}</p>
            </div>
          )}
          {!isLoading && reading && <p className="reading">{reading}</p>}
        </div>
  
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
