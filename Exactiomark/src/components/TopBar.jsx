import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Bell } from 'lucide-react';

export default function TopBar({ title }) {
    const { user } = useAuth();
    const navigate = useNavigate();

    return (
        <header className="topbar">
            <h1 className="topbar-title">{title}</h1>
            <div className="topbar-right">
                <button className="btn btn-secondary btn-sm" style={{ borderRadius: '50%', width: 36, height: 36, padding: 0 }}>
                    <Bell size={18} />
                </button>
                <div
                    className="topbar-user topbar-user-clickable"
                    onClick={() => navigate('/profile')}
                    title="View Profile"
                >
                    <div className="topbar-avatar">{user?.avatar}</div>
                    <span className="topbar-username">{user?.name}</span>
                </div>
            </div>
        </header>
    );
}
