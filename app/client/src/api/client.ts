// API client configuration

// Base URL configuration - works in both dev and production
const API_BASE_URL = import.meta.env.DEV 
  ? '/api'  // Proxy to backend in development
  : 'http://localhost:8000/api';  // Direct backend in production

// Generic API request function
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

// API methods
export const api = {
  // Upload file
  async uploadFile(file: File): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    return apiRequest<FileUploadResponse>('/upload', {
      method: 'POST',
      body: formData
    });
  },
  
  // Process query
  async processQuery(request: QueryRequest): Promise<QueryResponse> {
    return apiRequest<QueryResponse>('/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    });
  },
  
  // Get database schema
  async getSchema(): Promise<DatabaseSchemaResponse> {
    return apiRequest<DatabaseSchemaResponse>('/schema');
  },
  
  // Generate insights
  async generateInsights(request: InsightsRequest): Promise<InsightsResponse> {
    return apiRequest<InsightsResponse>('/insights', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    });
  },
  
  // Health check
  async healthCheck(): Promise<HealthCheckResponse> {
    return apiRequest<HealthCheckResponse>('/health');
  },

  // Export table to CSV
  async exportTable(tableName: string): Promise<void> {
    const url = `${API_BASE_URL}/export/table/${tableName}`;

    try {
      const response = await fetch(url, {
        method: 'POST'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Get the CSV blob
      const blob = await response.blob();

      // Create a download link and trigger it
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `${tableName}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      console.error('Table export failed:', error);
      throw error;
    }
  },

  // Export query results to CSV
  async exportQueryResults(sql: string, results: Record<string, any>[], columns: string[]): Promise<void> {
    const url = `${API_BASE_URL}/export/results`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          sql,
          results,
          columns
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Get the CSV blob
      const blob = await response.blob();

      // Get filename from Content-Disposition header
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = 'query_results.csv';
      if (contentDisposition) {
        const matches = /filename=([^;]+)/.exec(contentDisposition);
        if (matches && matches[1]) {
          filename = matches[1];
        }
      }

      // Create a download link and trigger it
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      console.error('Query results export failed:', error);
      throw error;
    }
  }
};