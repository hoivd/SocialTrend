import os
from huggingface_hub import snapshot_download, hf_hub_download, list_repo_files
from typing import List

class HFDatasetCloner:
    def __init__(self, repo_id: str, repo_type: str = "dataset", token: str = None):
        """
        Khởi tạo class tải dataset từ Hugging Face.
        :param repo_id: Tên repo, ví dụ "hoivd/SocialData"
        :param repo_type: "dataset", "model", hoặc "space"
        :param token: (optional) token cá nhân nếu repo private
        """
        self.repo_id = repo_id
        self.repo_type = repo_type
        self.token = token

    def clone_all(self, local_dir: str = "./hf_data", use_lfs: bool = True) -> str:
        """
        Tải toàn bộ repo về máy.
        :param local_dir: Thư mục lưu dữ liệu
        :param use_lfs: Cho phép tải Git LFS files
        :return: Đường dẫn đến thư mục local
        """
        print(f"📦 Đang clone toàn bộ repo: {self.repo_id}")
        path = snapshot_download(
            repo_id=self.repo_id,
            repo_type=self.repo_type,
            local_dir=local_dir,
            force_download=True,
            max_workers=3,
            token=self.token
        )
        print(f"✅ Repo đã được tải về thư mục: {path}")
        return path

    def clone_file(self, filename: str, local_dir: str = "./hf_file") -> str:
        """
        Tải 1 file cụ thể từ repo.
        :param filename: Đường dẫn file trong repo (VD: 'data/train.json')
        :param local_dir: Thư mục lưu file
        :return: Đường dẫn file local đã tải
        """
        print(f"📄 Đang tải file: {filename}")
        file_path = hf_hub_download(
            repo_id=self.repo_id,
            filename=filename,
            repo_type=self.repo_type,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            token=self.token
        )
        print(f"✅ File đã được lưu tại: {file_path}")
        return file_path
    
    def clone_folder(self, folder_path: str, local_dir: str = "./hf_folder") -> List[str]:
        """
        Tải toàn bộ các file bên trong một thư mục cụ thể từ repo.
        :param folder_path: Thư mục trong repo, ví dụ 'data/json/'
        :param local_dir: Thư mục local để lưu các file
        :return: Danh sách đường dẫn các file đã tải
        """
        print(f"📂 Cloning folder: {folder_path}")
        all_files = list_repo_files(self.repo_id, repo_type=self.repo_type, token=self.token)
        target_files = [f for f in all_files if f.startswith(folder_path)]

        if not target_files:
            print(f"❌ Không tìm thấy thư mục hoặc file nào bắt đầu với: {folder_path}")
            return []

        os.makedirs(local_dir, exist_ok=True)
        downloaded_files = []

        for file in target_files:
            print(f"  ⬇️  Downloading: {file}")
            path = hf_hub_download(
                repo_id=self.repo_id,
                filename=file,
                repo_type=self.repo_type,
                local_dir=local_dir,
                local_dir_use_symlinks=False,
                token=self.token
            )
            downloaded_files.append(path)

        print(f"✅ Đã tải {len(downloaded_files)} file từ thư mục {folder_path}")
        return downloaded_files
    
if __name__ == "__main__":
    cloner = HFDatasetCloner("hoivd/SocialData")

    # Tải toàn bộ repo
    cloner.clone_all(local_dir="full_dataset")

    # Tải một file cụ thể
    cloner.clone_file("data/json/posts_beatvn.network.json", local_dir="./data/json")

    cloner.clone_folder("data", local_dir="all_data")