import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [filters, setFilters] = useState({
    enrollment_date: '',
    current_departments: [],
    current_programs: [],
    courses: [],
    citizenship: '',
    education_types: [],
    admission_bases: [],
    start_date: '',
    end_date: '',
    statuses: [],
    in_academic: false,
    expulsion_reasons: []
  });

  const [students, setStudents] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Загрузка кафедр
  useEffect(() => {
    const loadDepartments = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/departments/');
        setDepartments(response.data);
      } catch (err) {
        setError('Ошибка загрузки кафедр');
      }
    };
    loadDepartments();
  }, []);

  // Загрузка программ при изменении выбранных кафедр
    useEffect(() => {
      const loadPrograms = async () => {
        if (filters.current_departments.length > 0) {
          try {
            const response = await axios.get('http://localhost:8000/api/programs/', {
              params: {
                department_id: filters.current_departments.join(',')
              }
            });
            setPrograms(response.data);
          } catch (err) {
            setError('Ошибка загрузки направлений');
          }
        } else {
          setPrograms([]);
        }
      };
      loadPrograms();
    }, [filters.current_departments]);

  const handleFilterChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (type === 'checkbox') {
      setFilters(prev => {
        const newValues = checked
          ? [...prev[name], value]
          : prev[name].filter(v => v !== value);
        return { ...prev, [name]: newValues };
      });
    } else {
      setFilters(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Преобразуем массивы в строки для GET-параметров
      const params = {
        ...filters,
        current_departments: filters.current_departments.join(','),
        current_programs: filters.current_programs.join(','),
        courses: filters.courses.join(','),
        education_types: filters.education_types.join(','),
        admission_bases: filters.admission_bases.join(','),
        statuses: filters.statuses.join(','),
        expulsion_reasons: filters.expulsion_reasons.join(','),
      };

      // Удаляем пустые параметры
      Object.keys(params).forEach(key => {
        if (params[key] === '' || params[key] === []) {
          delete params[key];
        }
      });

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
      current_departments: [],
      current_programs: [],
      courses: [],
      citizenship: '',
      education_types: [],
      admission_bases: [],
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
        {/* Блок дат */}
        <div className="filter-section">
          <h3>Даты</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Конкретная дата зачисления:</label>
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
        </div>

        {/* Блок кафедр и программ */}
        <div className="filter-section">
          <h3>Кафедры и направления</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Кафедры:</label>
              <div className="checkbox-group">
                {departments.map(dept => (
                  <label key={dept.id}>
                    <input
                      type="checkbox"
                      name="current_departments"
                      value={dept.id}
                      checked={filters.current_departments.includes(String(dept.id))}
                      onChange={handleFilterChange}
                    />
                    {dept.name}
                  </label>
                ))}
              </div>
            </div>
            <div className="checkbox-group">
              {programs.filter(prog => prog.name && prog.name.trim() !== "").map(prog => (
                <label key={prog.id}>
                  <input
                    type="checkbox"
                    name="current_programs"
                    value={prog.id}
                    checked={filters.current_programs.includes(String(prog.id))}
                    onChange={handleFilterChange}
                    disabled={filters.current_departments.length === 0}
                  />
                  {prog.name}
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Блок курсов и гражданства */}
        <div className="filter-section">
          <h3>Курсы и гражданство</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Курсы:</label>
              <div className="checkbox-group">
                {[1, 2, 3, 4, 5, 6].map(course => (
                  <label key={course}>
                    <input
                      type="checkbox"
                      name="courses"
                      value={course}
                      checked={filters.courses.includes(String(course))}
                      onChange={handleFilterChange}
                    />
                    {course}
                  </label>
                ))}
              </div>
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
        </div>

        {/* Блок типа обучения и основания поступления */}
        <div className="filter-section">
          <h3>Тип обучения и основание поступления</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Тип обучения:</label>
              <div className="checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    name="education_types"
                    value="budget"
                    checked={filters.education_types.includes('budget')}
                    onChange={handleFilterChange}
                  />
                  Бюджет
                </label>
                <label>
                  <input
                    type="checkbox"
                    name="education_types"
                    value="contract"
                    checked={filters.education_types.includes('contract')}
                    onChange={handleFilterChange}
                  />
                  Контракт
                </label>
              </div>
            </div>
            <div className="form-group">
              <label>Основание поступления:</label>
              <div className="checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    name="admission_bases"
                    value="general"
                    checked={filters.admission_bases.includes('general')}
                    onChange={handleFilterChange}
                  />
                  Общий конкурс
                </label>
                <label>
                  <input
                    type="checkbox"
                    name="admission_bases"
                    value="target"
                    checked={filters.admission_bases.includes('target')}
                    onChange={handleFilterChange}
                  />
                  Целевое
                </label>
                <label>
                  <input
                    type="checkbox"
                    name="admission_bases"
                    value="quota"
                    checked={filters.admission_bases.includes('quota')}
                    onChange={handleFilterChange}
                  />
                  Квота
                </label>
              </div>
            </div>
          </div>
        </div>

        <div className="filter-section">
          <h3>Статус студента</h3>
          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                name="statuses"
                value="active"
                checked={filters.statuses.includes('active')}
                onChange={handleFilterChange}
              />
              Обучается
            </label>
            <label>
              <input
                type="checkbox"
                name="statuses"
                value="academic"
                checked={filters.statuses.includes('academic')}
                onChange={handleFilterChange}
              />
              В академе
            </label>
            <label>
              <input
                type="checkbox"
                name="statuses"
                value="graduated"
                checked={filters.statuses.includes('graduated')}
                onChange={handleFilterChange}
              />
              Выпускники
            </label>
            <label>
              <input
                type="checkbox"
                name="statuses"
                value="expelled"
                checked={filters.statuses.includes('expelled')}
                onChange={handleFilterChange}
              />
              Отчисленные
            </label>
          </div>
        </div>

        <div className="filter-section">
          <h3>Причина отчисления (если применимо)</h3>
          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                name="expulsion_reasons"
                value="own_desire"
                checked={filters.expulsion_reasons.includes('own_desire')}
                onChange={handleFilterChange}
              />
              По собственному желанию
            </label>
            <label>
              <input
                type="checkbox"
                name="expulsion_reasons"
                value="transfer"
                checked={filters.expulsion_reasons.includes('transfer')}
                onChange={handleFilterChange}
              />
              По переводу
            </label>
            <label>
              <input
                type="checkbox"
                name="expulsion_reasons"
                value="academic_failure"
                checked={filters.expulsion_reasons.includes('academic_failure')}
                onChange={handleFilterChange}
              />
              За неуспеваемость
            </label>
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
                <th>Кафедра</th>
                <th>Направление</th>
                <th>Курс</th>
                <th>Тип обучения</th>
                <th>Основание</th>
                <th>Гражданство</th>
                <th>Дата зачисления</th>
              </tr>
            </thead>
            <tbody>
              {students.map(student => (
                <tr key={student.id}>
                  <td>{student.last_name} {student.first_name} {student.middle_name}</td>
                  <td>{student.current_department?.name || 'Не указано'}</td>
                  <td>{student.current_program?.name || 'Не указано'}</td>
                  <td>{student.course}</td>
                  <td>{student.education_type_display}</td>
                  <td>{student.admission_basis_display}</td>
                  <td>{student.citizenship}</td>
                  <td>{student.enrollment_date}</td>
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