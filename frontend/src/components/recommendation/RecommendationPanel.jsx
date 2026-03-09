import React from 'react';
import { ThumbsUp, ThumbsDown, AlertCircle, FileSearch, IndianRupee } from 'lucide-react';

const RecommendationPanel = ({ data }) => {
    // Mock data logic for recommendation
    const riskSignals = data?.structured_signals?.structured_financial_analysis?.risk_summary || {
        circular_trading_risk: true,
        revenue_mismatch_risk: false,
        income_inconsistency_risk: false
    };

    const hasHighRisk = riskSignals.circular_trading_risk || riskSignals.revenue_mismatch_risk;
    const hasModerateRisk = riskSignals.income_inconsistency_risk;

    let recommendation = 'Review';
    let colorClass = 'blue';
    let Icon = FileSearch;

    if (hasHighRisk) {
        recommendation = 'Reject';
        colorClass = 'red';
        Icon = ThumbsDown;
    } else if (!hasModerateRisk && !hasHighRisk) {
        recommendation = 'Approve';
        colorClass = 'green';
        Icon = ThumbsUp;
    }

    const suggestedLimit = hasHighRisk ? 0 : hasModerateRisk ? 500000 : 1500000;

    return (
        <div className="max-w-4xl mx-auto px-4 py-8">
            <div className={`bg-white rounded-2xl shadow-lg border-2 border-${colorClass}-100 overflow-hidden`}>
                {/* Header Ribbon */}
                <div className={`bg-${colorClass}-50 px-6 py-4 border-b border-${colorClass}-100 flex items-center justify-between`}>
                    <h2 className="text-xl font-display font-semibold text-gray-900">Final Credit Decision</h2>
                    <span className={`inline-flex items-center space-x-2 px-4 py-2 rounded-full border border-${colorClass}-200 bg-white text-${colorClass}-700 font-bold uppercase tracking-wide text-sm`}>
                        <Icon className="w-5 h-5 mr-1" />
                        {recommendation}
                    </span>
                </div>

                <div className="p-8">
                    <div className="flex flex-col md:flex-row gap-8">

                        {/* Limit Recommendation */}
                        <div className="flex-1 bg-gray-50 rounded-xl p-6 border border-gray-100 flex flex-col justify-center items-center text-center">
                            <p className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Suggested Credit Limit</p>
                            <div className="flex items-center text-gray-900">
                                <IndianRupee className="w-8 h-8 text-gray-400 mr-1" />
                                <span className="text-4xl font-display font-bold">
                                    {suggestedLimit.toLocaleString('en-IN')}
                                </span>
                            </div>
                        </div>

                        {/* Explanation */}
                        <div className="flex-[2] space-y-4">
                            <h3 className="text-lg font-semibold text-gray-900">Decision Rationale</h3>
                            <p className="text-gray-600 leading-relaxed">
                                {recommendation === 'Reject' && "The application exceeds our risk tolerance due to critical flags identified in the financial data. Strong recommendation to decline the facility."}
                                {recommendation === 'Review' && "The application shows moderate risk indicators. Further manual investigation into income consistency is required before final approval."}
                                {recommendation === 'Approve' && "The applicant presents a strong credit profile with low risk indicators across structural and unstructured analyses. Facility is recommended for approval."}
                            </p>

                            {/* Risk Summary Pills */}
                            <div className="flex flex-wrap gap-2 pt-4">
                                <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${riskSignals.circular_trading_risk ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-600'}`}>
                                    Circular Trading
                                </span>
                                <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${riskSignals.revenue_mismatch_risk ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-600'}`}>
                                    Revenue Mismatch
                                </span>
                                <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${riskSignals.income_inconsistency_risk ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-600'}`}>
                                    Income Consistency
                                </span>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    );
};

export default RecommendationPanel;
