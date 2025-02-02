export default function AddModal({ isOpen, modal_id, setClose}) {
    if (!isOpen) return null
    return (
  
      <div className="fixed inset-0 bg-[#1E88E5]/10 backdrop-blur-sm flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl w-[60%] h-[50%] mx-auto shadow-xl relative">
          <button
            onClick={() => setClose()}
            className="absolute top-4 right-4 text-[#90CAF9] hover:text-[#1E88E5] transition-colors outline-none"
            aria-label="Close modal"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <div className="p-6 flex flex-col items-center">
            <h2 className="text-xl font-semibold text-[#1E88E5] mb-4"></h2>
  
            <p className="text-[#90CAF9] text-center mb-6">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Eius aliquam laudantium explicabo pariatur iste
              dolorem animi vitae error totam. At sapiente aliquam accusamus facere veritatis.
            </p>
  
            <div className="flex gap-4 w-full">
              <button
                onClick={() => setClose(false)}
                className="flex-1 px-4 py-2.5 border border-[#90CAF9] text-[#1E88E5] rounded-lg hover:bg-[#E3F2FD] font-medium transition-colors"
              >
                Cancel
              </button>
              <button
              //   onClick={onDeactivate}()
                className="flex-1 px-4 py-2.5 bg-[#1E88E5] text-white rounded-lg hover:bg-[#1976D2] font-medium transition-colors"
              >
                Deactivate
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }
  