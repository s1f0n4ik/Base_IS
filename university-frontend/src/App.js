// App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [date, setDate] = useState('');
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(`http://localhost:8000/api/enrollment-stats/?date=${date}`);
      setStats(response.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Произошла ошибка');
      setStats(null);
    }
  };

  return (
    <div className="container">
      <h1>Статистика зачисления студентов</h1>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="date">Дата зачисления:</label>
          <input
            type="date"
            id="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn">Получить статистику</button>
      </form>

      {error && <div className="error">{error}</div>}

      {stats && (
        <div className="results">
          <h2>Результаты</h2>
          <p>Дата: {stats.date}</p>
          <p>Количество зачисленных: {stats.count}</p>
          
          {stats.count > 0 && (
            <>
              <h3>Список студентов:</h3>
              <table>
                <thead>
                  <tr>
                    <th>ФИО</th>
                    <th>Факультет</th>
                    <th>Направление</th>
                    <th>Курс</th>
                    <th>Гражданство</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.students.map(student => (
                    <tr key={student.id}>
                      <td>{student.last_name} {student.first_name} {student.middle_name}</td>
                      <td>{student.faculty}</td>
                      <td>{student.program}</td>
                      <td>{student.course}</td>
                      <td>{student.citizenship}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;