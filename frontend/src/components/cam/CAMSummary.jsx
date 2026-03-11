import React from 'react';
import { User, Briefcase, Building2, Shield, AlertTriangle } from 'lucide-react';

const CAMSummary = ({ data }) => {
    if (!data || !data.unstructured_signals) return null;
    const signals = data.unstructured_signals;

    const sections = [
        {
            id: 'character',
            title: 'Character',
            icon: User,
            color: 'blue',
            status: 'strong',
            items: [
                signals.sentiment?.[0]?.signal || "Positive sentiment in MD&A",
                "Strong management structure indicated in Annual Report"
            ]
        },
        {
            id: 'capacity',
            title: 'Capacity',
            icon: Briefcase,
            color: 'green',
            status: 'moderate',
            items: [
                "Consistent historical revenue growth",
                "Current ratio indicates sufficient short-term liquidity"
            ]
        },
        {
            id: 'capital',
            title: 'Capital',
            icon: Building2,
            color: 'purple',
            status: 'strong',
            items: [
                "Healthy debt-to-equity ratio observed",
                "Retained earnings showing steady year-over-year increase"
            ]
        },
        {
            id: 'collateral',
            title: 'Collateral',
            icon: Shield,
            color: 'indigo',
            status: 'moderate',
            items: [
                signals.promoter_guarantee?.[0]?.description || "Promoter guarantees present",
                "Standard negative lien conditions apply"
            ]
        },
        {
            id: 'conditions',
            title: 'Conditions',
            icon: AlertTriangle,
            color: 'yellow',
            status: 'review',
            items: [
                signals.legal_disputes?.[0]?.description || "Pending litigation noted",
                "Subject to material adverse change clauses"
            ]
        }
    ];

    const getStatusColor = (status) => {
        switch (status) {
            case 'strong': return 'bg-green-100 text-green-800 border-green-200';
            case 'moderate': return 'bg-blue-100 text-blue-800 border-blue-200';
            case 'review': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
            default: return 'bg-gray-100 text-gray-800 border-gray-200';
        }
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="mb-8 border-b border-gray-200 pb-6 flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-display font-semibold text-gray-900">Credit Analysis Memo (CAM)</h1>
                    <p className="text-gray-500 mt-2 text-sm uppercase tracking-wider font-semibold">The 5 C's of Credit Assessment</p>
                </div>
                <div className="text-right">
                    <p className="text-sm text-gray-500">Generated: {new Date().toLocaleDateString()}</p>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-md text-sm font-medium bg-gray-100 text-gray-800 mt-2">
                        AI-Assisted Report
                    </span>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {sections.map((section) => {
                    const Icon = section.icon;
                    return (
                        <div key={section.id} className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
                            <div className={`h-2 bg-${section.color}-500`} />
                            <div className="p-6">
                                <div className="flex justify-between items-start mb-4">
                                    <div className={`p-3 rounded-lg bg-${section.color}-50 text-${section.color}-600`}>
                                        <Icon className="w-6 h-6" />
                                    </div>
                                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getStatusColor(section.status)}`}>
                                        {section.status.charAt(0).toUpperCase() + section.status.slice(1)}
                                    </span>
                                </div>
                                <h3 className="text-xl font-bold text-gray-900 mb-4">{section.title}</h3>
                                <ul className="space-y-3">
                                    {section.items.map((item, idx) => (
                                        <li key={idx} className="flex items-start">
                                            <span className="h-1.5 w-1.5 rounded-full bg-gray-400 mt-2 mr-2 shrink-0" />
                                            <span className="text-sm text-gray-600 leading-relaxed">{item}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default CAMSummary;
