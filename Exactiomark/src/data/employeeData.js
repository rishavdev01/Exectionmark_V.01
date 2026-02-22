/* ── Shared employee data store ── 
   Used by HREmployees, HRPromotions, and EmployeeProfile */

export const employees = [
    {
        id: 1, name: 'Vikram Singh', role: 'Developer', dept: 'Engineering', avatar: 'VS',
        email: 'vikram.singh@exactiomark.com', phone: '+91 98765 43210',
        projects: ['Sprint Alpha', 'Sprint Beta'], status: 'Active',
        perfScore: 89.2, behaviour: 8.5, risk: 'Low', sprintContrib: '24 SP',
        alignment: 91, onTime: 94, rejection: 5,
        alignmentHistory: [
            { sprint: 'S1', score: 78 }, { sprint: 'S2', score: 82 }, { sprint: 'S3', score: 85 },
            { sprint: 'S4', score: 88 }, { sprint: 'S5', score: 90 }, { sprint: 'S6', score: 91 },
        ],
        sprintTrend: [
            { sprint: 'S1', sp: 18 }, { sprint: 'S2', sp: 22 }, { sprint: 'S3', sp: 20 },
            { sprint: 'S4', sp: 24 }, { sprint: 'S5', sp: 21 }, { sprint: 'S6', sp: 26 },
        ],
        behaviourScores: { communication: 9, ownership: 9, teamwork: 8, leadership: 7, discipline: 9 },
        managerComment: 'Consistently delivers high-quality code. Excellent problem solver and proactive communicator.',
        riskData: { overloadFreq: 2, escalationInvolvement: 1, perfDrop: -3.2 },
        promotion: { eligible: true, aiVerdict: 'Strongly Recommend', managerReview: 'Approved', finalDecision: 'Promoted', lastReview: 'Feb 15, 2026', reviewedBy: 'Priya Sharma' },
    },
    {
        id: 2, name: 'Sneha Iyer', role: 'Scrum Master', dept: 'Engineering', avatar: 'SI',
        email: 'sneha.iyer@exactiomark.com', phone: '+91 98765 43211',
        projects: ['Sprint Alpha'], status: 'Active',
        perfScore: 86.8, behaviour: 9.0, risk: 'Low', sprintContrib: '18 SP',
        alignment: 87, onTime: 88, rejection: 8,
        alignmentHistory: [
            { sprint: 'S1', score: 80 }, { sprint: 'S2', score: 83 }, { sprint: 'S3', score: 84 },
            { sprint: 'S4', score: 86 }, { sprint: 'S5', score: 85 }, { sprint: 'S6', score: 87 },
        ],
        sprintTrend: [
            { sprint: 'S1', sp: 14 }, { sprint: 'S2', sp: 16 }, { sprint: 'S3', sp: 18 },
            { sprint: 'S4', sp: 17 }, { sprint: 'S5', sp: 19 }, { sprint: 'S6', sp: 18 },
        ],
        behaviourScores: { communication: 9, ownership: 8, teamwork: 9, leadership: 8, discipline: 9 },
        managerComment: 'Great facilitator. Improved code review throughput significantly this sprint.',
        riskData: { overloadFreq: 0, escalationInvolvement: 0, perfDrop: 1.5 },
        promotion: { eligible: true, aiVerdict: 'Recommend', managerReview: 'Pending', finalDecision: '—', lastReview: '—', reviewedBy: '—' },
    },
    {
        id: 3, name: 'Ananya Reddy', role: 'DevOps Engineer', dept: 'Infrastructure', avatar: 'AR',
        email: 'ananya.reddy@exactiomark.com', phone: '+91 98765 43212',
        projects: ['Sprint Alpha', 'Sprint Gamma'], status: 'Active',
        perfScore: 74.3, behaviour: 7.5, risk: 'High', sprintContrib: '21 SP',
        alignment: 78, onTime: 72, rejection: 15,
        alignmentHistory: [
            { sprint: 'S1', score: 82 }, { sprint: 'S2', score: 80 }, { sprint: 'S3', score: 78 },
            { sprint: 'S4', score: 76 }, { sprint: 'S5', score: 75 }, { sprint: 'S6', score: 78 },
        ],
        sprintTrend: [
            { sprint: 'S1', sp: 20 }, { sprint: 'S2', sp: 22 }, { sprint: 'S3', sp: 25 },
            { sprint: 'S4', sp: 23 }, { sprint: 'S5', sp: 20 }, { sprint: 'S6', sp: 21 },
        ],
        behaviourScores: { communication: 7, ownership: 8, teamwork: 7, leadership: 6, discipline: 8 },
        managerComment: 'Technically strong but workload management needs support. Needs better task estimation.',
        riskData: { overloadFreq: 5, escalationInvolvement: 3, perfDrop: -7.8 },
        promotion: { eligible: false, aiVerdict: 'Not Recommended', managerReview: 'Hold', finalDecision: 'Hold', lastReview: 'Feb 14, 2026', reviewedBy: 'Arjun Patel' },
    },
    {
        id: 4, name: 'Arjun Patel', role: 'Sprint Master', dept: 'Management', avatar: 'AP',
        email: 'arjun.patel@exactiomark.com', phone: '+91 98765 43213',
        projects: ['Sprint Alpha'], status: 'Active',
        perfScore: 85.5, behaviour: 8.8, risk: 'Low', sprintContrib: '—',
        alignment: 85, onTime: 90, rejection: 6,
        alignmentHistory: [
            { sprint: 'S1', score: 80 }, { sprint: 'S2', score: 82 }, { sprint: 'S3', score: 84 },
            { sprint: 'S4', score: 83 }, { sprint: 'S5', score: 86 }, { sprint: 'S6', score: 85 },
        ],
        sprintTrend: [
            { sprint: 'S1', sp: 0 }, { sprint: 'S2', sp: 0 }, { sprint: 'S3', sp: 0 },
            { sprint: 'S4', sp: 0 }, { sprint: 'S5', sp: 0 }, { sprint: 'S6', sp: 0 },
        ],
        behaviourScores: { communication: 9, ownership: 9, teamwork: 9, leadership: 8, discipline: 9 },
        managerComment: 'Excellent sprint management skills. Keeps team motivated and aligned.',
        riskData: { overloadFreq: 1, escalationInvolvement: 2, perfDrop: 0.5 },
        promotion: { eligible: true, aiVerdict: 'Recommend', managerReview: 'Approved', finalDecision: 'Pending', lastReview: 'Feb 18, 2026', reviewedBy: 'Rajesh Mehta' },
    },
    {
        id: 5, name: 'Priya Sharma', role: 'HR Manager', dept: 'Human Resources', avatar: 'PS',
        email: 'priya.sharma@exactiomark.com', phone: '+91 98765 43214',
        projects: ['—'], status: 'Active',
        perfScore: 88.1, behaviour: 9.2, risk: 'Low', sprintContrib: '—',
        alignment: 82, onTime: 95, rejection: 3,
        alignmentHistory: [
            { sprint: 'S1', score: 75 }, { sprint: 'S2', score: 78 }, { sprint: 'S3', score: 80 },
            { sprint: 'S4', score: 81 }, { sprint: 'S5', score: 83 }, { sprint: 'S6', score: 82 },
        ],
        sprintTrend: [
            { sprint: 'S1', sp: 0 }, { sprint: 'S2', sp: 0 }, { sprint: 'S3', sp: 0 },
            { sprint: 'S4', sp: 0 }, { sprint: 'S5', sp: 0 }, { sprint: 'S6', sp: 0 },
        ],
        behaviourScores: { communication: 10, ownership: 9, teamwork: 9, leadership: 9, discipline: 9 },
        managerComment: 'Outstanding HR leadership. Drives culture and process improvements.',
        riskData: { overloadFreq: 0, escalationInvolvement: 0, perfDrop: 2.1 },
        promotion: { eligible: true, aiVerdict: 'Strongly Recommend', managerReview: 'Approved', finalDecision: 'Promoted', lastReview: 'Feb 12, 2026', reviewedBy: 'Rajesh Mehta' },
    },
    {
        id: 6, name: 'Rahul Verma', role: 'Developer', dept: 'Engineering', avatar: 'RV',
        email: 'rahul.verma@exactiomark.com', phone: '+91 98765 43215',
        projects: ['Sprint Beta'], status: 'Probation',
        perfScore: 72.1, behaviour: 6.8, risk: 'Medium', sprintContrib: '14 SP',
        alignment: 70, onTime: 68, rejection: 18,
        alignmentHistory: [
            { sprint: 'S1', score: 75 }, { sprint: 'S2', score: 72 }, { sprint: 'S3', score: 70 },
            { sprint: 'S4', score: 68 }, { sprint: 'S5', score: 71 }, { sprint: 'S6', score: 70 },
        ],
        sprintTrend: [
            { sprint: 'S1', sp: 12 }, { sprint: 'S2', sp: 10 }, { sprint: 'S3', sp: 14 },
            { sprint: 'S4', sp: 11 }, { sprint: 'S5', sp: 13 }, { sprint: 'S6', sp: 14 },
        ],
        behaviourScores: { communication: 6, ownership: 7, teamwork: 7, leadership: 5, discipline: 7 },
        managerComment: 'Needs improvement on code quality and delivery timelines. Frequent rework cycles.',
        riskData: { overloadFreq: 3, escalationInvolvement: 2, perfDrop: -5.4 },
        promotion: { eligible: false, aiVerdict: 'Not Recommended', managerReview: 'Hold', finalDecision: 'Hold', lastReview: 'Feb 10, 2026', reviewedBy: 'Sneha Iyer' },
    },
    {
        id: 7, name: 'Meera Nair', role: 'QA Engineer', dept: 'Quality', avatar: 'MN',
        email: 'meera.nair@exactiomark.com', phone: '+91 98765 43216',
        projects: ['Sprint Alpha'], status: 'Active',
        perfScore: 81.4, behaviour: 8.0, risk: 'Low', sprintContrib: '16 SP',
        alignment: 83, onTime: 85, rejection: 7,
        alignmentHistory: [
            { sprint: 'S1', score: 78 }, { sprint: 'S2', score: 80 }, { sprint: 'S3', score: 81 },
            { sprint: 'S4', score: 82 }, { sprint: 'S5', score: 84 }, { sprint: 'S6', score: 83 },
        ],
        sprintTrend: [
            { sprint: 'S1', sp: 12 }, { sprint: 'S2', sp: 14 }, { sprint: 'S3', sp: 15 },
            { sprint: 'S4', sp: 14 }, { sprint: 'S5', sp: 16 }, { sprint: 'S6', sp: 16 },
        ],
        behaviourScores: { communication: 8, ownership: 8, teamwork: 8, leadership: 7, discipline: 8 },
        managerComment: 'Thorough testing approach. Good eye for edge cases. Growing into leadership.',
        riskData: { overloadFreq: 1, escalationInvolvement: 0, perfDrop: 1.2 },
        promotion: { eligible: true, aiVerdict: 'Recommend', managerReview: 'Pending', finalDecision: '—', lastReview: '—', reviewedBy: '—' },
    },
    {
        id: 8, name: 'Karan Joshi', role: 'Developer', dept: 'Engineering', avatar: 'KJ',
        email: 'karan.joshi@exactiomark.com', phone: '+91 98765 43217',
        projects: ['Sprint Gamma'], status: 'On Leave',
        perfScore: 68.5, behaviour: 7.2, risk: 'High', sprintContrib: '10 SP',
        alignment: 65, onTime: 62, rejection: 20,
        alignmentHistory: [
            { sprint: 'S1', score: 72 }, { sprint: 'S2', score: 70 }, { sprint: 'S3', score: 68 },
            { sprint: 'S4', score: 66 }, { sprint: 'S5', score: 64 }, { sprint: 'S6', score: 65 },
        ],
        sprintTrend: [
            { sprint: 'S1', sp: 14 }, { sprint: 'S2', sp: 12 }, { sprint: 'S3', sp: 11 },
            { sprint: 'S4', sp: 10 }, { sprint: 'S5', sp: 9 }, { sprint: 'S6', sp: 10 },
        ],
        behaviourScores: { communication: 7, ownership: 7, teamwork: 7, leadership: 5, discipline: 7 },
        managerComment: 'Performance declining. Currently on leave. Need 1-on-1 after return.',
        riskData: { overloadFreq: 4, escalationInvolvement: 3, perfDrop: -9.1 },
        promotion: { eligible: false, aiVerdict: 'Not Recommended', managerReview: 'Hold', finalDecision: 'Hold', lastReview: 'Feb 8, 2026', reviewedBy: 'Sneha Iyer' },
    },
];

export const getEmployee = (id) => employees.find(e => e.id === Number(id));
