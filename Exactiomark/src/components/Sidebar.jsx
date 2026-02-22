import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { NAVIGATION } from '../data/navigation';
import * as Icons from 'lucide-react';
import { LogOut } from 'lucide-react';

export default function Sidebar() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const role = user?.role || '';
    const navItems = NAVIGATION[role] || [];

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const getIcon = (iconName) => {
        const Icon = Icons[iconName];
        return Icon ? <Icon size={20} className="nav-icon" /> : null;
    };

    return (
        <aside className="sidebar">
            {/* Brand */}
            <div className="sidebar-brand">
                <div className="sidebar-brand-sub">Company Portal</div>
                <div className="sidebar-brand-name">Exactiomark</div>
            </div>

            {/* Navigation */}
            <nav className="sidebar-nav">
                {navItems.map((item, i) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `sidebar-nav-item ${isActive ? 'active' : ''}`
                        }
                        style={{ animationDelay: `${i * 0.04}s` }}
                    >
                        {getIcon(item.icon)}
                        <span>{item.label}</span>
                    </NavLink>
                ))}
            </nav>

            {/* Logout Button */}
            <div className="sidebar-logout">
                <button className="sidebar-logout-btn" onClick={handleLogout}>
                    <LogOut size={20} />
                    <span>Logout</span>
                </button>
            </div>
        </aside>
    );
}
