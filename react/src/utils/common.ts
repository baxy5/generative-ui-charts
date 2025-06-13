// Helper function to convert a File to a base64 string to be able to proccess on the backend
export const toBase64 = (file: File) =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      const encoded = reader.result?.toString().split(",")[1];
      resolve(encoded);
    };
    reader.onerror = (err) => reject(err);
  });
