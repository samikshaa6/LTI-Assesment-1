const API_BASE = "http://localhost:8000";

export const uploadFiles = async (resume: File, jd: File) => {
    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("jd", jd);

    const response = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
    });
    return response.json();
};

export const chatWithResume = async (question: string) => {
    const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
    });
    return response.json();
};
