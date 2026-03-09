import React from 'react';
import { ShieldAlert, TrendingUp, AlertCircle, FileText, CheckCircle2 } from 'lucide-react';

const Dashboard = ({ data }) => {
    // Mock data if no backend data is provided
    const metrics = data?.structured_signals?.structured_financial_analysis || {
        financial_summary: { gst_sales: 2000000, bank_inflows: 1700000, itr_income: 900000 },
        circular_trading: { circular_trading_detected: true },
        revenue_mismatch: { ratio: 0.85, revenue_inflation_flag: false },
        income_consistency: { income_ratio: 0.45, income_inconsistency_flag: false }
    };

    const riskScore = 68; // Mock risk score

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(amount);
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Header Section */}
            <div className="mb-8">
                <h1 className="text-2xl font-semibold text-gray-900">Financial Risk Dashboard</h1>
                <p className="text-gray-500 mt-1">Real-time analysis and signals from borrower data</p>
            </div>

            {/* Credit Risk Score Gauge */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 mb-8 flex flex-col items-center justify-center">
                <h2 className="text-lg font-medium text-gray-700 mb-6 font-display">Credit Risk Score</h2>
                <div className="relative w-48 h-48 flex items-center justify-center">
                    {/* Progress Circle SVG */}
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="#f1f5f9" strokeWidth="10" />
                        <circle
                            cx="50" cy="50" r="45"
                            fill="none"
                            stroke="#f59e0b" // Yellow/Orange for moderate risk
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

            {/* Financial Metrics Cards */}
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Financial Overview</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between mb-4">
                        <div className="bg-blue-50 p-3 rounded-lg text-primary-600">
                            <TrendingUp className="w-6 h-6" />
                        </div>
                        <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">GST Data</span>
                    </div>
                    <p className="text-sm text-gray-500 mb-1">Total Sales</p>
                    <h3 className="text-2xl font-bold text-gray-900 font-display">{formatCurrency(metrics.financial_summary.gst_sales)}</h3>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between mb-4">
                        <div className="bg-blue-50 p-3 rounded-lg text-primary-600">
                            <fileText className="w-6 h-6" />
                        </div>
                        <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Bank Data</span>
                    </div>
                    <p className="text-sm text-gray-500 mb-1">Total Inflows</p>
                    <h3 className="text-2xl font-bold text-gray-900 font-display">{formatCurrency(metrics.financial_summary.bank_inflows)}</h3>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between mb-4">
                        <div className="bg-blue-50 p-3 rounded-lg text-primary-600">
                            <FileText className="w-6 h-6" />
                        </div>
                        <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">ITR Data</span>
                    </div>
                    <p className="text-sm text-gray-500 mb-1">Reported Income</p>
                    <h3 className="text-2xl font-bold text-gray-900 font-display">{formatCurrency(metrics.financial_summary.itr_income)}</h3>
                </div>
            </div>

            {/* Risk Indicators */}
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Risk Profile</h2>
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden mb-8">
                <div className="divide-y divide-gray-100">

                    <div className="p-4 sm:p-6 flex flex-col sm:flex-row sm:items-center justify-between hover:bg-gray-50 transition-colors">
                        <div className="flex items-start space-x-4">
                            <div className={`mt-1 p-2 rounded-lg ${metrics.circular_trading.circular_trading_detected ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}`}>
                                {metrics.circular_trading.circular_trading_detected ? <ShieldAlert className="w-5 h-5" /> : <CheckCircle2 className="w-5 h-5" />}
                            </div>
                            <div>
                                <h3 className="text-base font-semibold text-gray-900">Circular Trading</h3>
                                <p className="text-sm text-gray-500">Analysis of trading cycles across multiple GSTNs.</p>
                            </div>
                        </div>
                        <div className="mt-4 sm:mt-0 flex shrink-0">
                            {metrics.circular_trading.circular_trading_detected ? (
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

                    <div className="p-4 sm:p-6 flex flex-col sm:flex-row sm:items-center justify-between hover:bg-gray-50 transition-colors">
                        <div className="flex items-start space-x-4">
                            <div className={`mt-1 p-2 rounded-lg ${metrics.revenue_mismatch.revenue_inflation_flag ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}`}>
                                {metrics.revenue_mismatch.revenue_inflation_flag ? <AlertCircle className="w-5 h-5" /> : <CheckCircle2 className="w-5 h-5" />}
                            </div>
                            <div>
                                <h3 className="text-base font-semibold text-gray-900">Revenue Mismatch</h3>
                                <p className="text-sm text-gray-500">Comparison of GST Sales to Bank Inflows (Ratio: {metrics.revenue_mismatch.ratio.toFixed(2)}).</p>
                            </div>
                        </div>
                        <div className="mt-4 sm:mt-0 flex shrink-0">
                            {metrics.revenue_mismatch.revenue_inflation_flag ? (
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

                    <div className="p-4 sm:p-6 flex flex-col sm:flex-row sm:items-center justify-between hover:bg-gray-50 transition-colors">
                        <div className="flex items-start space-x-4">
                            <div className={`mt-1 p-2 rounded-lg ${metrics.income_consistency.income_inconsistency_flag ? 'bg-yellow-50 text-yellow-600' : 'bg-green-50 text-green-600'}`}>
                                {metrics.income_consistency.income_inconsistency_flag ? <AlertCircle className="w-5 h-5" /> : <CheckCircle2 className="w-5 h-5" />}
                            </div>
                            <div>
                                <h3 className="text-base font-semibold text-gray-900">Income Consistency</h3>
                                <p className="text-sm text-gray-500">Comparison of GST Sales vs ITR Reported Income.</p>
                            </div>
                        </div>
                        <div className="mt-4 sm:mt-0 flex shrink-0">
                            {metrics.income_consistency.income_inconsistency_flag ? (
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

                </div>
            </div>
        </div>
    );
};

export default Dashboard;
