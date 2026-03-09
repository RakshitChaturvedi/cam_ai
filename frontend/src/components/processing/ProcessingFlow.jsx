import React, { useState, useEffect } from 'react';
import { FileUp, FileText, Activity, BarChart2, CheckCircle2, ChevronRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ProcessingFlow = ({ onComplete }) => {
    const [currentStep, setCurrentStep] = useState(0);

    const steps = [
        { id: 1, title: 'PDF Parsing', icon: FileUp, description: 'Extracting text and structure from raw documents.' },
        { id: 2, title: 'Classification', icon: FileText, description: 'Identifying document types (Annual Report, Legal, etc.).' },
        { id: 3, title: 'Signal Extraction', icon: Activity, description: 'Using LLMs to pull risk signals from text.' },
        { id: 4, title: 'Financial Analysis', icon: BarChart2, description: 'Normalizing and evaluating structured data.' },
    ];

    useEffect(() => {
        if (currentStep < steps.length) {
            const timer = setTimeout(() => {
                setCurrentStep(prev => prev + 1);
            }, 2000); // 2 seconds per mock step
            return () => clearTimeout(timer);
        } else {
            setTimeout(() => {
                if (onComplete) onComplete();
            }, 1000);
        }
    }, [currentStep, steps.length, onComplete]);

    return (
        <div className="max-w-4xl mx-auto px-4 py-16">
            <div className="text-center mb-12">
                <h2 className="text-3xl font-display font-bold text-gray-900 mb-4">Processing Pipeline</h2>
                <p className="text-gray-500 max-w-2xl mx-auto">Our AI engine is currently synthesizing unstructured and structured data points to build a comprehensive risk profile.</p>
            </div>

            <div className="relative">
                {/* Connecting Line */}
                <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-gray-100 -translate-y-1/2" />
                <div
                    className="hidden md:block absolute top-1/2 left-0 h-0.5 bg-primary-500 transition-all duration-1000 ease-in-out -translate-y-1/2"
                    style={{ width: `${(Math.min(currentStep, steps.length - 1) / (steps.length - 1)) * 100}%` }}
                />

                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative z-10">
                    {steps.map((step, index) => {
                        const Icon = step.icon;
                        const isCompleted = currentStep > index;
                        const isActive = currentStep === index;

                        return (
                            <div key={step.id} className="flex flex-col items-center relative">
                                <motion.div
                                    initial={{ scale: 0.8, opacity: 0 }}
                                    animate={{ scale: 1, opacity: 1 }}
                                    transition={{ delay: index * 0.2 }}
                                    className={`w-16 h-16 rounded-2xl flex items-center justify-center shadow-lg transition-colors duration-500 mb-4
                    ${isCompleted ? 'bg-green-500 text-white shadow-green-500/30' :
                                            isActive ? 'bg-primary-600 text-white shadow-primary-600/30 animate-pulse' :
                                                'bg-white text-gray-400 border-2 border-gray-100'}`}
                                >
                                    {isCompleted ? <CheckCircle2 className="w-8 h-8" /> : <Icon className="w-8 h-8" />}
                                </motion.div>

                                <h3 className={`font-semibold text-center mb-2 ${isActive ? 'text-primary-600' : isCompleted ? 'text-gray-900' : 'text-gray-400'}`}>
                                    {step.title}
                                </h3>
                                <p className="text-xs text-center text-gray-500 max-w-[150px]">
                                    {step.description}
                                </p>

                                {/* Mobile connecting line */}
                                {index < steps.length - 1 && (
                                    <div className="md:hidden flex justify-center my-4">
                                        <ChevronRight className={`w-6 h-6 ${isCompleted ? 'text-green-500' : 'text-gray-200'}`} />
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};

export default ProcessingFlow;
