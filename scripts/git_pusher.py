import git
import os

def push_to_github(access_token, local_repo_path, branch_name, commit_message="Update code", remote_url: str = "https://github.com/hoivd/SocialTrend"):
    try:
        # Kiểm tra nếu thư mục tồn tại
        if not os.path.exists(local_repo_path):
            raise FileNotFoundError(f"Thư mục '{local_repo_path}' không tồn tại.")
        
        # Mở repository đã clone
        repo = git.Repo(local_repo_path)

        # Chèn access token vào remote_url
        if remote_url.startswith("https://"):
            token_url = remote_url.replace("https://", f"https://hoivd:{access_token}@")
        else:
            raise ValueError("Remote URL phải dùng giao thức HTTPS.")

        # Thiết lập hoặc cập nhật remote "origin"
        if "origin" in repo.remotes:
            repo.remote("origin").set_url(token_url)
        else:
            repo.create_remote("origin", url=token_url)

        # Tạo và checkout branch mới
        if branch_name in repo.heads:
            print(f"⚠️ Branch '{branch_name}' đã tồn tại. Checkout...")
            repo.git.checkout(branch_name)
        else:
            print(f"📌 Tạo branch mới '{branch_name}' và checkout...")
            repo.git.checkout('-b', branch_name)

        # Add tất cả thay đổi
        repo.git.add(all=True)

        # Commit nếu có thay đổi
        if repo.is_dirty(untracked_files=True):
            repo.index.commit(commit_message)
            print(f"✅ Commit: {commit_message}")
        else:
            print("⚠️ Không có thay đổi nào để commit.")

        # Push branch lên remote
        repo.git.push('--set-upstream', 'origin', branch_name)
        print(f"🚀 Đã push branch '{branch_name}' lên GitHub thành công.")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    access_token = os.getenv("GITHUB_TOKEN")
    print(access_token)
    local_repo_path = r"D:\\DS200.P21\\SocialTrend"
    branch_name = "my-feature-branch"

    push_to_github(access_token, local_repo_path, branch_name)