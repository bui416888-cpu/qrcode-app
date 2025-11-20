import qrcode
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def generate_qr():
    url = entry_url.get()
    if not url:
        messagebox.showwarning("提示", "请输入网址！")
        return
        
    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data
        qr.add_data(url)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white")

        # Generate filename based on timestamp
        timestamp = int(time.time())
        filename = f"qrcode_{timestamp}.png"
        
        # Save the image
        img.save(filename)
        
        # Convert to PhotoImage for Tkinter
        # We need to resize it to fit the window if it's too big, but for now let's keep it original size
        # or resize for display purposes. Let's resize for better UI fit.
        display_img = img.resize((250, 250))
        tk_img = ImageTk.PhotoImage(display_img)
        
        # Update label
        label_img.config(image=tk_img)
        label_img.image = tk_img # Keep a reference!
        
        # Show success message (optional, maybe just status bar or keep popup)
        # User asked for "directly display", maybe popup is annoying if it blocks view?
        # But requirement said "save ... and popup" in previous turn, this turn says "display ... and save".
        # I will keep the popup as it confirms saving.
        messagebox.showinfo("成功", f"二维码已生成并保存为 {filename}")
        
    except Exception as e:
        messagebox.showerror("错误", f"发生错误: {e}")

if __name__ == "__main__":
    # Create main window
    root = tk.Tk()
    root.title("马尊二维码神器")
    root.geometry("500x600") # Increased height for image

    # Title Label
    label_title = tk.Label(root, text="马尊二维码神器", font=("Arial", 20, "bold"))
    label_title.pack(pady=20)

    # Input Frame
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    label_instruction = tk.Label(input_frame, text="网址:", font=("Arial", 12))
    label_instruction.pack(side=tk.LEFT, padx=5)

    entry_url = tk.Entry(input_frame, width=40, font=("Arial", 12))
    entry_url.pack(side=tk.LEFT, padx=5)

    # Button
    btn_generate = tk.Button(root, text="生成二维码", command=generate_qr, font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=15)
    btn_generate.pack(pady=20)

    # Image Label (Placeholder)
    label_img = tk.Label(root)
    label_img.pack(pady=10, expand=True)

    # Start the GUI event loop
    root.mainloop()
