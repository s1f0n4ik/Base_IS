import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [filters, setFilters] = useState({
    enrollment_date: '',
    faculty_id: '',
    program_id: '',
    course: '',
    citizenship: '',
    start_date: '',
    end_date: '',
  });
  const [students, setStudents] = useState([]);
  const [faculties, setFaculties] = useState([]);
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Загрузка факультетов при монтировании
  useEffect(() => {
    const loadFaculties = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/faculties/');
        setFaculties(response.data);
      } catch (err) {
        setError('Ошибка загрузки факультетов');
      }
    };
    loadFaculties();
  }, []);

  // Загрузка программ при изменении выбранного факультета
  useEffect(() => {
    const loadPrograms = async () => {
      if (filters.faculty_id) {
        try {
          const response = await axios.get(`http://localhost:8000/api/programs/?faculty_id=${filters.faculty_id}`);
          setPrograms(response.data);
        } catch (err) {
          setError('Ошибка загрузки направлений');
        }
      } else {
        setPrograms([]);
      }
    };
    loadPrograms();
  }, [filters.faculty_id]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value,
      // Сбрасываем program_id при изменении факультета
      ...(name === 'faculty_id' && { program_id: '' }),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Удаляем пустые параметры фильтрации
      const params = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v !== '')
      );

      const response = await axios.get('http://localhost:8000/api/students/', { params });
      setStudents(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Произошла ошибка');
      setStudents([]);
    } finally {
      setLoading(false);
    }
  };

  const resetFilters = () => {
    setFilters({
      enrollment_date: '',
      faculty_id: '',
      program_id: '',
      course: '',
      citizenship: '',
      start_date: '',
      end_date: '',
    });
    setStudents([]);
    setError('');
  };

  return (
    <div className="container">
      <h1>Информационная система университета</h1>

      <form onSubmit={handleSubmit} className="filter-form">
        <div className="form-row">
          <div className="form-group">
            <label>Дата зачисления:</label>
            <input
              type="date"
              name="enrollment_date"
              value={filters.enrollment_date}
              onChange={handleFilterChange}
            />
          </div>

          <div className="form-group">
            <label>Период зачисления:</label>
            <div className="date-range">
              <input
                type="date"
                name="start_date"
                value={filters.start_date}
                onChange={handleFilterChange}
                placeholder="С"
              />
              <input
                type="date"
                name="end_date"
                value={filters.end_date}
                onChange={handleFilterChange}
                placeholder="По"
              />
            </div>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Факультет:</label>
            <select
              name="faculty_id"
              value={filters.faculty_id}
              onChange={handleFilterChange}
            >
              <option value="">Все факультеты</option>
              {faculties.map(faculty => (
                <option key={faculty.id} value={faculty.id}>
                  {faculty.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Направление:</label>
            <select
              name="program_id"
              value={filters.program_id}
              onChange={handleFilterChange}
              disabled={!filters.faculty_id}
            >
              <option value="">Все направления</option>
              {programs.map(program => (
                <option key={program.id} value={program.id}>
                  {program.name} ({program.faculty.name})
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Курс:</label>
            <select
              name="course"
              value={filters.course}
              onChange={handleFilterChange}
            >
              <option value="">Все курсы</option>
              {[1, 2, 3, 4, 5, 6].map(course => (
                <option key={course} value={course}>{course}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Гражданство:</label>
            <input
              type="text"
              name="citizenship"
              value={filters.citizenship}
              onChange={handleFilterChange}
              placeholder="Введите гражданство"
            />
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn" disabled={loading}>
            {loading ? 'Загрузка...' : 'Применить фильтры'}
          </button>
          <button type="button" className="btn btn-secondary" onClick={resetFilters}>
            Сбросить фильтры
          </button>
        </div>
      </form>

      {error && <div className="error">{error}</div>}

      <div className="results">
        <h2>Результаты ({students.length} студентов)</h2>

        {students.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>ФИО</th>
                <th>Дата зачисления</th>
                <th>Дата отчисления</th>
                <th>Факультет</th>
                <th>Направление</th>
                <th>Курс</th>
                <th>Гражданство</th>
              </tr>
            </thead>
            <tbody>
              {students.map(student => (
                <tr key={student.id}>
                  <td>{student.last_name} {student.first_name} {student.middle_name}</td>
                  <td>{student.enrollment_date}</td>
                  <td>{student.expulsion_date || '-'}</td>
                  <td>{student.faculty.name}</td>
                  <td>{student.program.name}</td>
                  <td>{student.course}</td>
                  <td>{student.citizenship}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          !loading && <p>Нет данных для отображения. Примените фильтры.</p>
        )}
      </div>
    </div>
  );
}

export default App;