import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentUser } from '../../api/auth';
import { removeToken } from '../../utils/auth';
import './styles.css';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      setLoading(true);
      const userData = await getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Ошибка загрузки пользователя:', error);
      if (error.response && error.response.status === 401) {
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    removeToken();
    navigate('/login');
  };

  const handleBackToChat = () => {
    navigate('/chat');
  };

  if (loading) {
    return (
      <div className="profile-container" data-easytag="id1-react/src/components/Profile/index.jsx">
        <div className="loading-screen">
          <div className="spinner"></div>
          <p>Загрузка...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container" data-easytag="id1-react/src/components/Profile/index.jsx">
      <div className="profile-content">
        <div className="profile-card">
          <div className="profile-header">
            <div className="avatar">
              {user?.username?.charAt(0).toUpperCase()}
            </div>
            <h1 className="profile-title">Профиль</h1>
          </div>

          <div className="profile-info">
            <div className="info-label">Имя пользователя</div>
            <div className="info-value">{user?.username}</div>
          </div>

          <div className="info-label" style={{ marginTop: '20px' }}>ID пользователя</div>
          <div className="info-value">{user?.id}</div>

          <div className="profile-actions">
            <button
              className="chat-button"
              onClick={handleBackToChat}
              type="button"
            >
              Вернуться в чат
            </button>
            <button
              className="logout-button"
              onClick={handleLogout}
              type="button"
            >
              Выйти
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
