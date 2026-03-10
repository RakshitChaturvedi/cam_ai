import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { UploadCloud, CheckCircle, Database, Loader2, Building2, User, Fingerprint, Hash } from 'lucide-react';

const FileUploadInput = ({ label, id, description, accept, fileState, onFileChange }) => (
    <div className="bg-white p-4 rounded-xl border border-gray-100 shadow-sm">
        <h3 className="text-sm font-semibold text-gray-800">{label}</h3>
        <p className="text-xs text-gray-500 mb-3">{description}</p>

        <div className="relative">
            <input
                type="file"
                id={id}
                accept={accept}
                onChange={(e) => onFileChange(e, id)}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            <div className={`flex items-center justify-center p-3 rounded-lg border-2 border-dashed transition-colors
                ${fileState ? 'border-primary-500 bg-primary-50' : 'border-gray-200 hover:border-primary-300'}`}>
                {fileState ? (
                    <div className="flex items-center text-primary-700">
                        <CheckCircle className="w-5 h-5 mr-2" />
                        <span className="text-sm font-medium truncate max-w-[150px]">{fileState.name}</span>
                    </div>
                ) : (
                    <div className="flex flex-col items-center text-gray-500">
                        <UploadCloud className="w-5 h-5 mb-1 text-gray-400" />
                        <span className="text-xs">Click to upload</span>
                    </div>
                )}
            </div>
        </div>
    </div>
);

const EntityDetailsCard = ({ entityData, isLoading }) => {
    if (isLoading) {
        return (
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 animate-pulse">
                <div className="flex items-center mb-4">
                    <div className="h-5 w-5 bg-gray-200 rounded mr-2"></div>
                    <div className="h-5 w-40 bg-gray-200 rounded"></div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                    {[1, 2, 3, 4].map(i => (
                        <div key={i}>
                            <div className="h-3 w-20 bg-gray-200 rounded mb-2"></div>
                            <div className="h-4 w-32 bg-gray-100 rounded"></div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    if (!entityData) return null;

    const entity = entityData.entity_details || {};
    const promoters = entityData.promoter_details || [];

    // Don't show card if no meaningful data
    if (!entity.company_name && !entity.company_pan && !entity.cin && promoters.length === 0) {
        return null;
    }

    return (
        <div className="bg-gradient-to-br from-white to-primary-50 rounded-xl border border-primary-100 shadow-md p-6">
            <div className="flex items-center mb-4">
                <Building2 className="w-5 h-5 text-primary-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">Identified Entity</h3>
                <span className="ml-auto text-xs font-medium bg-green-100 text-green-700 px-2 py-0.5 rounded-full">Extracted</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3 mb-4">
                {entity.company_name && (
                    <div className="sm:col-span-2">
                        <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">Company Name</p>
                        <p className="text-sm font-semibold text-gray-900">{entity.company_name}</p>
                    </div>
                )}
                {entity.company_pan && (
                    <div>
                        <p className="text-xs text-gray-500 uppercase tracking-wide font-medium flex items-center"><Fingerprint className="w-3 h-3 mr-1" />Company PAN</p>
                        <p className="text-sm font-mono font-semibold text-gray-800">{entity.company_pan}</p>
                    </div>
                )}
                {entity.cin && (
                    <div>
                        <p className="text-xs text-gray-500 uppercase tracking-wide font-medium flex items-center"><Hash className="w-3 h-3 mr-1" />CIN</p>
                        <p className="text-sm font-mono font-semibold text-gray-800">{entity.cin}</p>
                    </div>
                )}
            </div>

            {promoters.length > 0 && (
                <div className="border-t border-primary-100 pt-3">
                    <p className="text-xs text-gray-500 uppercase tracking-wide font-medium mb-2 flex items-center"><User className="w-3 h-3 mr-1" />Promoter Details</p>
                    <div className="space-y-2">
                        {promoters.map((p, idx) => (
                            <div key={idx} className="flex items-center justify-between bg-white/70 rounded-lg px-3 py-2 border border-gray-100">
                                <span className="text-sm font-medium text-gray-800">{p.name || 'Unknown'}</span>
                                <div className="flex space-x-3 text-xs text-gray-500">
                                    {p.din && <span>DIN: <span className="font-mono font-semibold text-gray-700">{p.din}</span></span>}
                                    {p.pan && <span>PAN: <span className="font-mono font-semibold text-gray-700">{p.pan}</span></span>}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

const FileUpload = ({ onUploadComplete }) => {
    const [files, setFiles] = useState({
        annual_report: null,
        legal_notice: null,
        sanction_letter: null,
        gst: null,
        bank: null,
        itr: null
    });
    const [entityData, setEntityData] = useState(null);
    const [isExtracting, setIsExtracting] = useState(false);
    const [hasTriggeredExtraction, setHasTriggeredExtraction] = useState(false);

    const handleFileChange = (e, key) => {
        if (e.target.files && e.target.files.length > 0) {
            setFiles(prev => ({
                ...prev,
                [key]: e.target.files[0]
            }));
        }
    };

    // Auto-trigger entity extraction when any unstructured file is uploaded
    const triggerEntityExtraction = useCallback(async (currentFiles) => {
        const hasUnstructured = currentFiles.annual_report || currentFiles.legal_notice || currentFiles.sanction_letter;
        if (!hasUnstructured || hasTriggeredExtraction) return;

        setIsExtracting(true);
        setHasTriggeredExtraction(true);

        try {
            const formData = new FormData();
            Object.keys(currentFiles).forEach(key => {
                if (currentFiles[key]) {
                    formData.append(key, currentFiles[key]);
                }
            });

            const response = await axios.post('http://localhost:8000/api/entity-extract', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setEntityData(response.data);
        } catch (err) {
            console.error('Entity extraction failed:', err);
        } finally {
            setIsExtracting(false);
        }
    }, [hasTriggeredExtraction]);

    // Watch for unstructured file additions
    useEffect(() => {
        triggerEntityExtraction(files);
    }, [files, triggerEntityExtraction]);

    const handleProceed = () => {
        onUploadComplete(files);
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-12">
            {/* Databricks Banner */}
            <div className="mb-8 bg-gradient-to-r from-gray-900 to-gray-800 rounded-xl p-4 flex items-center shadow-lg">
                <div className="flex items-center space-x-3 flex-1">
                    <div className="bg-orange-500/20 p-2 rounded-lg">
                        <Database className="w-6 h-6 text-orange-400" />
                    </div>
                    <div>
                        <p className="text-white font-semibold text-sm">Databricks Enterprise Data Lake</p>
                        <p className="text-gray-400 text-xs">Secure connection to centralized enterprise data warehouse</p>
                    </div>
                </div>
                <div className="flex items-center space-x-2 bg-gray-700/50 px-3 py-1.5 rounded-full">
                    <span className="relative flex h-2.5 w-2.5">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-500"></span>
                    </span>
                    <span className="text-green-400 text-xs font-medium">Connected</span>
                </div>
            </div>

            <div className="text-center mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">Upload Borrower Documents</h2>
                <p className="text-gray-500">Provide the unstructured and structured data required for CAM AI processing. You may skip files to use defaults.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div className="space-y-4">
                    <h3 className="text-lg font-medium text-gray-900 border-b pb-2">Unstructured Documents (PDF)</h3>
                    <FileUploadInput id="annual_report" label="Annual Report" description="Latest audited financial report" accept=".pdf" fileState={files['annual_report']} onFileChange={handleFileChange} />
                    <FileUploadInput id="legal_notice" label="Legal Notices" description="Any pending litigation or notices" accept=".pdf" fileState={files['legal_notice']} onFileChange={handleFileChange} />
                    <FileUploadInput id="sanction_letter" label="Sanction Letter" description="Previous loan sanction details" accept=".pdf" fileState={files['sanction_letter']} onFileChange={handleFileChange} />
                </div>
                <div className="space-y-4">
                    <h3 className="text-lg font-medium text-gray-900 border-b pb-2">Structured Data (CSV / PDF)</h3>
                    <FileUploadInput id="gst" label="GST Data" description="GST sales and filing history" accept=".csv,.pdf" fileState={files['gst']} onFileChange={handleFileChange} />
                    <FileUploadInput id="bank" label="Bank Statements" description="Transaction inflow/outflow data" accept=".csv,.pdf" fileState={files['bank']} onFileChange={handleFileChange} />
                    <FileUploadInput id="itr" label="ITR Data" description="Income Tax Return records" accept=".csv,.pdf" fileState={files['itr']} onFileChange={handleFileChange} />
                </div>
            </div>

            {/* Entity Details Card */}
            {(isExtracting || entityData) && (
                <div className="mb-8">
                    <EntityDetailsCard entityData={entityData} isLoading={isExtracting} />
                </div>
            )}

            <div className="flex justify-center">
                <button
                    onClick={handleProceed}
                    className="bg-primary-600 hover:bg-primary-700 text-white font-medium py-3 px-8 rounded-lg shadow-md transition-colors flex items-center"
                >
                    Analyze Documents
                </button>
            </div>
        </div>
    );
};

export default FileUpload;
