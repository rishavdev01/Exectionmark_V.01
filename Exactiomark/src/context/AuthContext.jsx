import { createContext, useContext, useState } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

/* ── Company-wide password (same for all employees) ── */
const COMPANY_PASSWORD = 'Exactio@org123';

/* ── Fallback users for offline/dev mode ── */
const MOCK_USERS = [
    { id: 'EMP-CEO-001', password: 'Emp@ceo123', name: 'ceo_admin', role: 'CEO', email: 'ceo@exactiomark.com', dept: 'Executive', avatar: 'CE' },
    { id: 'EMP-HR-001', password: 'Emp@hr123', name: 'hr_admin', role: 'HR', email: 'hr@exactiomark.com', dept: 'Human Resources', avatar: 'HR' },
    { id: 'EMP-PM-001', password: 'Emp@pm123', name: 'pm_admin', role: 'PM', email: 'pm@exactiomark.com', dept: 'Management', avatar: 'PM' },
    { id: 'EMP-LEAD-001', password: 'Emp@lead123', name: 'lead_admin', role: 'LEAD', email: 'lead@exactiomark.com', dept: 'Engineering', avatar: 'LA' },
    { id: 'EMP-DEV-001', password: 'Emp@dev123', name: 'dev_admin', role: 'DEVELOPER', email: 'dev@exactiomark.com', dept: 'Engineering', avatar: 'DA' },
    { id: 'EMP-OPS-001', password: 'Emp@ops123', name: 'ops_admin', role: 'DEVOPS', email: 'ops@exactiomark.com', dept: 'Infrastructure', avatar: 'OA' },
    { id: 'EMP-QA-001', password: 'Emp@qa123', name: 'qa_admin', role: 'QA', email: 'qa@exactiomark.com', dept: 'Quality Assurance', avatar: 'QA' },
];

export function AuthProvider({ children }) {
    const [user, setUser] = useState(() => {
        const saved = sessionStorage.getItem('exec_user');
        return saved ? JSON.parse(saved) : null;
    });

    const login = async (userId, companyPwd, personalPwd) => {
        /* Step 1 – validate company password client-side */
        if (companyPwd !== COMPANY_PASSWORD) {
            return { success: false, error: 'Invalid company password.' };
        }

        /* Step 2 – call backend API with all three fields */
        try {
            const data = await authAPI.login(
                userId.trim(),   // employee_id
                companyPwd,      // organisation_password
                personalPwd      // employee_password
            );
            if (data && data.employee_id) {
                setUser(data);
                sessionStorage.setItem('exec_user', JSON.stringify(data));
                return { success: true, user: data };
            }
            return { success: false, error: 'Invalid credentials.' };
        } catch (err) {
            /* Offline fallback — only used when backend is unreachable */
            console.warn('Backend login failed, falling back to MOCK_USERS:', err.message);
            const found = MOCK_USERS.find(
                u => u.id.toLowerCase() === userId.trim().toLowerCase() && u.password === personalPwd
            );
            if (!found) return { success: false, error: 'Invalid User ID or personal password.' };
            const { password: _, ...safeUser } = found;
            setUser(safeUser);
            sessionStorage.setItem('exec_user', JSON.stringify(safeUser));
            return { success: true, user: safeUser };
        }
    };

    const logout = () => {
        setUser(null);
        sessionStorage.removeItem('exec_user');
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error('useAuth must be used within AuthProvider');
    return ctx;
}

export { MOCK_USERS, COMPANY_PASSWORD };
