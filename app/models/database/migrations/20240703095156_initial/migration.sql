/*
  Warnings:

  - You are about to drop the column `asssetId` on the `AssetIsRequestBuy` table. All the data in the column will be lost.
  - Added the required column `assetId` to the `AssetIsRequestBuy` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "AssetIsRequestBuy" DROP CONSTRAINT "AssetIsRequestBuy_asssetId_fkey";

-- AlterTable
ALTER TABLE "AssetIsRequestBuy" DROP COLUMN "asssetId",
ADD COLUMN     "assetId" TEXT NOT NULL;

-- AddForeignKey
ALTER TABLE "AssetIsRequestBuy" ADD CONSTRAINT "AssetIsRequestBuy_assetId_fkey" FOREIGN KEY ("assetId") REFERENCES "Assets"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
