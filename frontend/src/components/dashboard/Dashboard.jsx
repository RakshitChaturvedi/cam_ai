import React from 'react';
import { ShieldAlert, TrendingUp, AlertCircle, FileText, CheckCircle2, Info } from 'lucide-react';

const Dashboard = ({ data }) => {
    if (!data || !data.structured_signals) {
        return (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-8 text-center">
                    <Info className="w-8 h-8 text-yellow-500 mx-auto mb-3" />
                    <h2 className="text-lg font-semibold text-gray-900 mb-1">No Data Available</h2>
                    <p className="text-gray-500">Upload documents and run the analysis to see results here.</p>
                </div>
            </div>
        );
    }

    const metrics = data.structured_signals.structured_financial_analysis || {};
    const financial_summary = metrics.financial_summary || {};
    const circular_trading = metrics.circular_trading || {};
    const revenue_mismatch = metrics.revenue_mismatch || {};
    const income_consistency = metrics.income_consistency || {};

    const riskScore = data.recommendation_payload?.ml_confidence_score ?
        parseFloat(data.recommendation_payload.ml_confidence_score.replace('%', '')) : 0;

    const formatCurrency = (amount) => {
        if (amount === undefined || amount === null || amount === 0) return null;
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(amount);
    };

    const hasGstData = financial_summary.gst_sales > 0;
    const hasBankData = financial_summary.bank_inflows > 0;
    const hasItrData = financial_summary.itr_income > 0;
    const hasAnyFinancialData = hasGstData || hasBankData || hasItrData;

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Header Section */}
            <div className="mb-8">
                <h1 className="text-2xl font-semibold text-gray-900">Financial Risk Dashboard</h1>
                <p className="text-gray-500 mt-1">Real-time analysis and signals from borrower data</p>
            </div>

            {/* Credit Risk Score Gauge */}
            {riskScore > 0 && (
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 mb-8 flex flex-col items-center justify-center">
                    <h2 className="text-lg font-medium text-gray-700 mb-6 font-display">Credit Risk Score</h2>
                    <div className="relative w-48 h-48 flex items-center justify-center">
                        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                            <circle cx="50" cy="50" r="45" fill="none" stroke="#f1f5f9" strokeWidth="10" />
                            <circle
                                cx="50" cy="50" r="45"
                                fill="none"
                                stroke="#f59e0b"
                                strokeWidth="10"
                                strokeDasharray={`${(riskScore / 100) * 283} 283`}
                                strokeLinecap="round"
                                className="transition-all duration-1000 ease-out"
                            />
                        </svg>
                        <div className="absolute flex flex-col items-center justify-center text-center">
                            <span className="text-4xl font-bold text-gray-900">{riskScore}</span>
                            <span className="text-sm text-gray-500">/ 100</span>
                        </div>
                    </div>
                    <div className="mt-6 flex items-center justify-center space-x-2 bg-yellow-50 text-yellow-700 px-4 py-2 rounded-full font-medium">
                        <AlertCircle className="w-4 h-4" />
                        <span>Moderate Risk</span>
                    </div>
                </div>
            )}

            {/* Financial Metrics Cards */}
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Financial Overview</h2>
            {hasAnyFinancialData ? (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    {hasGstData && (
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                            <div className="flex items-center justify-between mb-4">
                                <div className="bg-blue-50 p-3 rounded-lg text-primary-600">
                                    <TrendingUp className="w-6 h-6" />
                                </div>
                                <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">GST Data</span>
                            </div>
                            <p className="text-sm text-gray-500 mb-1">Total Sales</p>
                            <h3 className="text-2xl font-bold text-gray-900 font-display">{formatCurrency(financial_summary.gst_sales)}</h3>
                        </div>
                    )}

                    {hasBankData && (
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                            <div className="flex items-center justify-between mb-4">
                                <div className="bg-blue-50 p-3 rounded-lg text-primary-600">
                                    <FileText className="w-6 h-6" />
                                </div>
                                <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Bank Data</span>
                            </div>
                            <p className="text-sm text-gray-500 mb-1">Total Inflows</p>
                            <h3 className="text-2xl font-bold text-gray-900 font-display">{formatCurrency(financial_summary.bank_inflows)}</h3>
                        </div>
                    )}

                    {hasItrData && (
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                            <div className="flex items-center justify-between mb-4">
                                <div className="bg-blue-50 p-3 rounded-lg text-primary-600">
                                    <FileText className="w-6 h-6" />
                                </div>
                                <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">ITR Data</span>
                            </div>
                            <p className="text-sm text-gray-500 mb-1">Reported Income</p>
                            <h3 className="text-2xl font-bold text-gray-900 font-display">{formatCurrency(financial_summary.itr_income)}</h3>
                        </div>
                    )}
                </div>
            ) : (
                <div className="bg-gray-50 border border-gray-200 rounded-xl p-6 mb-8 text-center">
                    <p className="text-gray-500">No structured financial data uploaded. Upload GST, Bank, or ITR files to see the overview.</p>
                </div>
            )}

            {/* Risk Indicators */}
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Risk Profile</h2>
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden mb-8">
                <div className="divide-y divide-gray-100">

                    {/* Circular Trading - only show if GST data was analyzed */}
                    {!circular_trading.not_analyzed && (
                        <div className="p-4 sm:p-6 flex flex-col sm:flex-row sm:items-center justify-between hover:bg-gray-50 transition-colors">
                            <div className="flex items-start space-x-4">
                                <div className={`mt-1 p-2 rounded-lg ${circular_trading.circular_trading_detected ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}`}>
                                    {circular_trading.circular_trading_detected ? <ShieldAlert className="w-5 h-5" /> : <CheckCircle2 className="w-5 h-5" />}
                                </div>
                                <div>
                                    <h3 className="text-base font-semibold text-gray-900">Circular Trading</h3>
                                    <p className="text-sm text-gray-500">Analysis of trading cycles across multiple GSTNs.</p>
                                </div>
                            </div>
                            <div className="mt-4 sm:mt-0 flex shrink-0">
                                {circular_trading.circular_trading_detected ? (
                                    <span className="inline-flex items-center rounded-full bg-red-100 px-3 py-1 text-sm font-medium text-red-800">
                                        High Risk Detected
                                    </span>
                                ) : (
                                    <span className="inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800">
                                        Low Risk
                                    </span>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Revenue Mismatch - only show if GST or Bank data was analyzed */}
                    {!revenue_mismatch.not_analyzed && (
                        <div className="p-4 sm:p-6 flex flex-col sm:flex-row sm:items-center justify-between hover:bg-gray-50 transition-colors">
                            <div className="flex items-start space-x-4">
                                <div className={`mt-1 p-2 rounded-lg ${revenue_mismatch.revenue_inflation_flag ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}`}>
                                    {revenue_mismatch.revenue_inflation_flag ? <AlertCircle className="w-5 h-5" /> : <CheckCircle2 className="w-5 h-5" />}
                                </div>
                                <div>
                                    <h3 className="text-base font-semibold text-gray-900">Revenue Mismatch</h3>
                                    <p className="text-sm text-gray-500">Comparison of GST Sales to Bank Inflows (Ratio: {revenue_mismatch.ratio?.toFixed(2) || 'N/A'}).</p>
                                </div>
                            </div>
                            <div className="mt-4 sm:mt-0 flex shrink-0">
                                {revenue_mismatch.revenue_inflation_flag ? (
                                    <span className="inline-flex items-center rounded-full bg-red-100 px-3 py-1 text-sm font-medium text-red-800">
                                        Mismatch Detected
                                    </span>
                                ) : (
                                    <span className="inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800">
                                        Consistent
                                    </span>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Income Consistency - only show if GST or ITR data was analyzed */}
                    {!income_consistency.not_analyzed && (
                        <div className="p-4 sm:p-6 flex flex-col sm:flex-row sm:items-center justify-between hover:bg-gray-50 transition-colors">
                            <div className="flex items-start space-x-4">
                                <div className={`mt-1 p-2 rounded-lg ${income_consistency.income_inconsistency_flag ? 'bg-yellow-50 text-yellow-600' : 'bg-green-50 text-green-600'}`}>
                                    {income_consistency.income_inconsistency_flag ? <AlertCircle className="w-5 h-5" /> : <CheckCircle2 className="w-5 h-5" />}
                                </div>
                                <div>
                                    <h3 className="text-base font-semibold text-gray-900">Income Consistency</h3>
                                    <p className="text-sm text-gray-500">Comparison of GST Sales vs ITR Reported Income.</p>
                                </div>
                            </div>
                            <div className="mt-4 sm:mt-0 flex shrink-0">
                                {income_consistency.income_inconsistency_flag ? (
                                    <span className="inline-flex items-center rounded-full bg-yellow-100 px-3 py-1 text-sm font-medium text-yellow-800">
                                        Review Required
                                    </span>
                                ) : (
                                    <span className="inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800">
                                        Low Risk
                                    </span>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Show message when no risk analyses were performed */}
                    {circular_trading.not_analyzed && revenue_mismatch.not_analyzed && income_consistency.not_analyzed && (
                        <div className="p-6 text-center">
                            <p className="text-gray-500">No structured data uploaded for risk analysis. Upload GST, Bank, or ITR files to see risk indicators.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
