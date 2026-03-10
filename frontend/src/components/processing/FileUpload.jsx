import React, { useState } from 'react';
import { UploadCloud, CheckCircle } from 'lucide-react';

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

const FileUpload = ({ onUploadComplete }) => {
    const [files, setFiles] = useState({
        annual_report: null,
        legal_notice: null,
        sanction_letter: null,
        gst: null,
        bank: null,
        itr: null
    });

    const handleFileChange = (e, key) => {
        if (e.target.files && e.target.files.length > 0) {
            setFiles(prev => ({
                ...prev,
                [key]: e.target.files[0]
            }));
        }
    };

    const handleProceed = () => {
        onUploadComplete(files);
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-12">
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
