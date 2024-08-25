/*
  Warnings:

  - You are about to drop the column `asssetId` on the `AssetIsSell` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[assetId]` on the table `AssetIsSell` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `assetId` to the `AssetIsSell` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "AssetIsSell" DROP CONSTRAINT "AssetIsSell_asssetId_fkey";

-- DropIndex
DROP INDEX "AssetIsSell_asssetId_key";

-- AlterTable
ALTER TABLE "AssetIsSell" DROP COLUMN "asssetId",
ADD COLUMN     "assetId" TEXT NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "AssetIsSell_assetId_key" ON "AssetIsSell"("assetId");

-- AddForeignKey
ALTER TABLE "AssetIsSell" ADD CONSTRAINT "AssetIsSell_assetId_fkey" FOREIGN KEY ("assetId") REFERENCES "Assets"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
