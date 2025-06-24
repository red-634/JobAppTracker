from tracker import add_job, list_jobs, update_status, clear_jobs, JOB_STAGES
import time

def show_menu():
    print("\n--- Job Application Tracker ---")
    print("1. Add new application")
    print("2. View all applications")
    print("3. Update application status")
    print("4. Clear an application (CAREFUL: This will delete data!)")
    print("5. Exit")


def display_jobs(jobs):
    if not jobs:
        print("No job applications found.")
    for idx, job in enumerate(jobs):
        print(f"{idx + 1}. {job['company']} - {job['role']} [{job['status']}] (Applied: {job['applied_date']})")


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            company = input("Enter company name: ")
            role = input("Enter role: ")
            add_job(company, role)
            print("Application added!!!!")
            print("--------------------------------------")

        elif choice == "2":
            jobs = list_jobs()
            display_jobs(jobs)
            print("--------------------------------------")

        elif choice == "3":
            jobs = list_jobs()
            display_jobs(jobs)
            if jobs:
                try:
                    idx = int(input("Enter job number to update: ")) - 1
                    print("Select new status:")
                    for i, stage in enumerate(JOB_STAGES):
                        print(f"{i + 1}. {stage}")
                    new_idx = int(input("Your choice: ")) - 1
                    update_status(idx, JOB_STAGES[new_idx])
                    print("🔁 Status updated!")
                    print("--------------------------------------")
                except (IndexError, ValueError):
                    print("❗ Invalid input.")

        elif choice == "4":
            confirm = input("Are you sure? This will delete an application. (yes/no): ")
            if confirm.lower() == "yes":
                
                jobs = list_jobs()
                if jobs:
                    try:
                        display_jobs(jobs)
                        idx = int(input("Enter job number to delete: ")) - 1
                        if idx < 0 or idx >= len(jobs):
                            print("❗ Invalid job number.")
                            continue
                        clear_jobs(int(idx))
                        print("Clearing application...")
                        time.sleep(1)  # Simulate a delay
                    except (IndexError, ValueError):
                        print("🔁 Status updated!")
                        print("--------------------------------------")
            else:
                print("Clear cancelled❗")
                print("--------------------------------------")
        
        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("❗ Invalid option. Try again.")


if __name__ == "__main__":
    main()
