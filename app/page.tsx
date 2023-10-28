'use client'
import Image from 'next/image'
import Link from 'next/link'
import { useState } from 'react';


export default function FileComparison() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [commonText, setCommonText] = useState('');

  const handleFile1Change = (e) => {
    setFile1(e.target.files[0]);
  };

  const handleFile2Change = (e) => {
    setFile2(e.target.files[0]);
  };

  const compareFiles = async () => {
    const formData = new FormData();
    formData.append('file1', file1);
    formData.append('file2', file2);

    try {
      const response = await fetch('/api/compare-files', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setCommonText(data.common_text);
      } else {
        console.error('API request failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>File Comparison</h2>
      <input type="file" onChange={handleFile1Change} />
      <input type="file" onChange={handleFile2Change} />
      <button onClick={compareFiles}>Compare Files</button>
      {commonText && (
        <div>
          <h3>Common Text:</h3>
          <pre>{commonText}</pre>
        </div>
      )}
    </div>
  );
}