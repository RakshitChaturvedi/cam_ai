import React, { useState } from 'react';
import axios from 'axios';
import {
    ClipboardEdit, Send, Loader2, TrendingUp, TrendingDown, Minus,
    FileText, AlertTriangle, CheckCircle2, ChevronRight, User
} from 'lucide-react';

const FIVE_CS = ['Character', 'Capacity', 'Capital', 'Collateral', 'Conditions'];

const SCORE_COLORS = {
    high: { bg: 'bg-green-50', text: 'text-green-700', bar: 'bg-green-500' },
    mid: { bg: 'bg-yellow-50', text: 'text-yellow-700', bar: 'bg-yellow-500' },
    low: { bg: 'bg-red-50', text: 'text-red-700', bar: 'bg-red-500' },
};

const getScoreStyle = (score) => {
    if (score >= 70) return SCORE_COLORS.high;
    if (score >= 40) return SCORE_COLORS.mid;
    return SCORE_COLORS.low;
};

const getSentimentIcon = (sentiment) => {
    if (!sentiment) return <Minus className="w-4 h-4 text-gray-400" />;
    const s = sentiment.toLowerCase();
    if (s === 'positive') return <TrendingUp className="w-4 h-4 text-green-500" />;
    if (s === 'negative') return <TrendingDown className="w-4 h-4 text-red-500" />;
    return <Minus className="w-4 h-4 text-gray-400" />;
};

const getSentimentBadge = (sentiment) => {
    if (!sentiment) return null;
    const s = sentiment.toLowerCase();
    const cls = s === 'positive' ? 'bg-green-100 text-green-700'
        : s === 'negative' ? 'bg-red-100 text-red-700'
            : 'bg-gray-100 text-gray-600';
    return <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${cls}`}>{sentiment}</span>;
};

const HITLPortal = ({ uploadedFiles, onComplete }) => {
    const [note, setNote] = useState('');
    const [source, setSource] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);
    const [scores, setScores] = useState({
        Character: 80, Capacity: 80, Capital: 80, Collateral: 80, Conditions: 80
    });
    const [submittedNotes, setSubmittedNotes] = useState([]);
    const [allAdjustmentLogs, setAllAdjustmentLogs] = useState([]);

    // Build source options from uploaded file names
    const sourceOptions = [];
    if (uploadedFiles) {
        const labelMap = {
            annual_report: 'Annual Report',
            legal_notice: 'Legal Notice',
            sanction_letter: 'Sanction Letter',
            gst: 'GST Data',
            bank: 'Bank Statement',
            itr: 'ITR Data'
        };
        Object.entries(uploadedFiles).forEach(([key, file]) => {
            if (file) {
                sourceOptions.push({
                    value: `${labelMap[key] || key} - ${file.name}`,
                    label: `${labelMap[key] || key} — ${file.name}`
                });
            }
        });
    }
    sourceOptions.push({ value: 'Field Visit', label: 'Field Visit' });
    sourceOptions.push({ value: 'General Observation', label: 'General Observation' });

    const handleSubmitNote = async () => {
        if (!note.trim()) return;

        setIsProcessing(true);
        try {
            const response = await axios.post('http://localhost:8000/api/hitl-process', {
                note: note.trim(),
                source: source || 'General Observation',
                baseline_scores: scores
            });

            const { nlp_extraction, adjusted_scores, adjustment_log } = response.data;

            setScores(adjusted_scores);
            setAllAdjustmentLogs(prev => [...prev, ...adjustment_log]);
            setSubmittedNotes(prev => [...prev, {
                text: note.trim(),
                source: source || 'General Observation',
                nlp: nlp_extraction,
                log: adjustment_log
            }]);
            setNote('');
        } catch (err) {
            console.error('HITL processing failed:', err);
        } finally {
            setIsProcessing(false);
        }
    };

    const handleProceed = () => {
        onComplete({
            adjusted_scores: scores,
            adjustment_log: allAdjustmentLogs
        });
    };

    return (
        <div className="max-w-5xl mx-auto px-4 py-10">
            {/* Header */}
            <div className="text-center mb-8">
                <div className="inline-flex items-center space-x-2 bg-amber-50 text-amber-700 px-4 py-1.5 rounded-full text-sm font-medium mb-4">
                    <User className="w-4 h-4" />
                    <span>Human-in-the-Loop Portal</span>
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Credit Officer Field Notes</h2>
                <p className="text-gray-500 max-w-2xl mx-auto">
                    Enter qualitative observations from field visits or document reviews. Each note is
                    analyzed by AI and deterministically mapped to credit score adjustments.
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left Column: Input + History */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Note Input Card */}
                    <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                        <h3 className="text-sm font-semibold text-gray-800 mb-4 flex items-center">
                            <ClipboardEdit className="w-4 h-4 mr-2 text-primary-600" />
                            Add Field Note
                        </h3>

                        <textarea
                            value={note}
                            onChange={(e) => setNote(e.target.value)}
                            placeholder="e.g. Factory visited on Tuesday. Operating at roughly 40% capacity, several assembly lines shut down."
                            className="w-full p-3 border border-gray-200 rounded-lg text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                            rows={3}
                        />

                        <div className="flex items-center justify-between mt-4 gap-4">
                            <div className="flex-1">
                                <label className="block text-xs font-medium text-gray-500 mb-1">Source Document</label>
                                <select
                                    value={source}
                                    onChange={(e) => setSource(e.target.value)}
                                    className="w-full p-2.5 border border-gray-200 rounded-lg text-sm text-gray-700 bg-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                                >
                                    <option value="">Select source...</option>
                                    {sourceOptions.map((opt, idx) => (
                                        <option key={idx} value={opt.value}>{opt.label}</option>
                                    ))}
                                </select>
                            </div>

                            <button
                                onClick={handleSubmitNote}
                                disabled={!note.trim() || isProcessing}
                                className="mt-5 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-2.5 px-6 rounded-lg shadow-sm transition-colors flex items-center text-sm"
                            >
                                {isProcessing ? (
                                    <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Analyzing...</>
                                ) : (
                                    <><Send className="w-4 h-4 mr-2" />Submit Note</>
                                )}
                            </button>
                        </div>
                    </div>

                    {/* Notes History */}
                    {submittedNotes.length > 0 && (
                        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                            <h3 className="text-sm font-semibold text-gray-800 mb-4">
                                Processed Notes ({submittedNotes.length})
                            </h3>
                            <div className="space-y-3">
                                {submittedNotes.map((entry, idx) => (
                                    <div key={idx} className="border border-gray-100 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                                        <div className="flex items-start justify-between mb-2">
                                            <p className="text-sm text-gray-800 flex-1 font-medium">"{entry.text}"</p>
                                            {getSentimentIcon(entry.nlp?.sentiment)}
                                        </div>
                                        <div className="flex flex-wrap gap-2 mt-2">
                                            <span className="text-xs bg-primary-50 text-primary-700 px-2 py-0.5 rounded-full font-medium">
                                                {entry.nlp?.mapped_category || 'Unknown'}
                                            </span>
                                            {getSentimentBadge(entry.nlp?.sentiment)}
                                            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                                                Severity: {entry.nlp?.severity_score || 0}/5
                                            </span>
                                            <span className="text-xs bg-blue-50 text-blue-600 px-2 py-0.5 rounded-full flex items-center">
                                                <FileText className="w-3 h-3 mr-1" />
                                                {entry.source}
                                            </span>
                                        </div>
                                        {entry.log?.length > 0 && (
                                            <div className="mt-2 text-xs text-gray-500 italic">
                                                {entry.log[0]}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* Right Column: Live 5C Scores */}
                <div className="space-y-6">
                    <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 sticky top-24">
                        <h3 className="text-sm font-semibold text-gray-800 mb-4">Live Credit Scores (5Cs)</h3>
                        <div className="space-y-4">
                            {FIVE_CS.map(c => {
                                const score = scores[c] || 0;
                                const style = getScoreStyle(score);
                                return (
                                    <div key={c}>
                                        <div className="flex items-center justify-between mb-1">
                                            <span className="text-sm font-medium text-gray-700">{c}</span>
                                            <span className={`text-sm font-bold ${style.text}`}>{score}</span>
                                        </div>
                                        <div className="w-full bg-gray-100 rounded-full h-2">
                                            <div
                                                className={`h-2 rounded-full transition-all duration-500 ${style.bar}`}
                                                style={{ width: `${Math.min(score, 100)}%` }}
                                            />
                                        </div>
                                    </div>
                                );
                            })}
                        </div>

                        <div className="mt-6 pt-4 border-t border-gray-100">
                            <div className="flex items-center justify-between mb-1">
                                <span className="text-xs text-gray-500">Composite Average</span>
                                <span className="text-sm font-bold text-gray-800">
                                    {Math.round(Object.values(scores).reduce((a, b) => a + b, 0) / FIVE_CS.length)}
                                </span>
                            </div>
                            <div className="text-xs text-gray-400 mt-1">
                                {submittedNotes.length === 0 ? 'No adjustments yet' : `${submittedNotes.length} note(s) applied`}
                            </div>
                        </div>
                    </div>

                    {/* Proceed Button */}
                    <button
                        onClick={handleProceed}
                        className="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-3 px-6 rounded-lg shadow-md transition-colors flex items-center justify-center"
                    >
                        Proceed to Analysis
                        <ChevronRight className="w-5 h-5 ml-1" />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default HITLPortal;
